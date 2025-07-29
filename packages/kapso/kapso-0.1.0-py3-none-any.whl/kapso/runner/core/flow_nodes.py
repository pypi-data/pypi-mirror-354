"""
Contains node agent creation and configuration functions.
"""

import logging
import uuid
import os
from typing import Callable, Dict, Any, Tuple, Optional

from langchain_core.messages import AIMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.types import Command

from kapso.runner.core.cache_utils import optimize_messages_for_provider
from kapso.runner.core.flow_state import State
from kapso.runner.core.flow_utils import get_next_pending_tool_call
from kapso.runner.core.llm_factory import initialize_llm
from kapso.runner.core.node_types.base import node_type_registry
from kapso.runner.core.tool_generator import (
    generate_tools_for_node,
    tool_requires_interrupt,
    get_interrupt_handler
)

# Create a logger for this module
logger = logging.getLogger(__name__)

# Lazy Redis client initialization
_redis_client: Optional[Any] = None

def get_redis_client():
    """Get Redis client if available, otherwise return None."""
    global _redis_client
    if _redis_client is None:
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            try:
                import redis
                _redis_client = redis.from_url(redis_url)
                logger.info("Redis client initialized successfully")
            except ImportError:
                logger.warning("Redis package not installed. Interrupt signals will be disabled.")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}. Interrupt signals will be disabled.")
    return _redis_client

def check_for_interrupt_signal(thread_id: str) -> Dict[str, bool]:
    """
    Check for interrupt signals for this thread.

    Returns:
        dict: Dictionary with signal types as keys and boolean values
              Example: {"new_message": True, "stop": False}
    """
    redis_client = get_redis_client()
    
    # If Redis is not available, return no signals
    if not redis_client:
        return {"new_message": False, "stop": False}
    
    try:
        signals = {
            "new_message": False,
            "stop": False
        }

        # Check for each signal type
        for signal_type in signals.keys():
            signal_key = f"signal:{thread_id}:{signal_type}"
            if redis_client.exists(signal_key):
                # Clear the signal
                redis_client.delete(signal_key)
                signals[signal_type] = True
                logger.info(f"{signal_type} signal detected and cleared for thread {thread_id}")

        return signals

    except Exception as e:
        logger.error(f"Error checking for interrupt signals for thread {thread_id}: {e}")
        return {"new_message": False, "stop": False}


def inject_handle_user_message_tool(state: State) -> Tuple[State, Dict[str, Any]]:
    """
    Inject a HandleUserMessage tool call into the state.

    Args:
        state: The current state

    Returns:
        A tuple of (modified_state, updates) where:
        - modified_state is the state with the tool call added
        - updates is a dict of updates for the Command
    """
    # Create a tool call for HandleUserMessage
    tool_call_id = str(uuid.uuid4())
    tool_call = {
        "id": tool_call_id,
        "name": "HandleUserMessage",
        "args": {}
    }

    # Create AI message with the tool call
    ai_message = AIMessage(
        content="",
        tool_calls=[tool_call]
    )

    # Prepare updates
    updates = {"full_history": [ai_message]}

    # Create modified state
    modified_state = state.copy()
    current_history = list(state.get("full_history", []))
    current_history.append(ai_message)
    modified_state["full_history"] = current_history

    return modified_state, updates


def inject_stop_execution_tool(state: State) -> Tuple[State, Dict[str, Any]]:
    """
    Inject a StopExecution tool call into the state.

    Args:
        state: The current state

    Returns:
        A tuple of (modified_state, updates) where:
        - modified_state is the state with the tool call added
        - updates is a dict of updates for the Command
    """
    # Create a tool call for StopExecution
    tool_call_id = str(uuid.uuid4())
    tool_call = {
        "id": tool_call_id,
        "name": "StopExecution",
        "args": {
            "reason": "Stop signal received"
        }
    }

    # Create AI message with the tool call
    ai_message = AIMessage(
        content="",
        tool_calls=[tool_call]
    )

    # Prepare updates
    updates = {"full_history": [ai_message]}

    # Create modified state
    modified_state = state.copy()
    current_history = list(state.get("full_history", []))
    current_history.append(ai_message)
    modified_state["full_history"] = current_history

    return modified_state, updates

async def handle_tool_call_routing(tool_call, current_node_name, node_type, node_name, node_config):
    """
    Determine routing for a tool call based on whether it requires a interrupt node.

    Args:
        tool_call: The tool call to handle
        current_node_name: The name of the current node
        node_type: The type of node
        node_name: The name of the node
        node_config: The configuration for the node

    Returns:
        A tuple of (state_update, next_node) where:
        - state_update is a dictionary of state updates to apply
        - next_node is the name of the node to route to, or None to stay in the current node
    """
    tool_name = tool_call["name"]

    # Initialize state update
    state_update = {}
    next_node = None

    # Generate tools to check for interrupt
    node_tools = await generate_tools_for_node(
        node_type=node_type,
        node_name=node_name,
        node_config=node_config
    )

    # Find the tool in all_tools
    tool = None
    for t in node_tools.get("all", []):
        if hasattr(t, "metadata") and hasattr(t.metadata, "name") and t.metadata.name == tool_name:
            tool = t
            break

    # Check if this tool requires a interrupt node
    if tool and tool_requires_interrupt(tool):
        logger.info(f"Tool {tool_name} requires a interrupt node")

        # Get handler name
        handler = get_interrupt_handler(tool)
        if handler:
            # Determine the next node based on the handler
            snake_case_tool_name = "".join(
                ["_" + c.lower() if c.isupper() else c for c in tool_name]
            ).lstrip("_")

            if tool_name == "AskUserForInput":
                message = tool_call["args"]["message"]
                logger.info("Routing to AskUserForInput with message: %s", message)
                state_update["conversation"] = [AIMessage(content=message)]
                next_node = f"{snake_case_tool_name}_{current_node_name}"
            elif tool_name == "SendWhatsappTemplateMessage":
                logger.info("Routing to SendWhatsappTemplateMessage")
                next_node = f"{snake_case_tool_name}_{current_node_name}"
            elif tool_name == "EnterIdleState":
                message = tool_call["args"]["message"]
                logger.info("Routing to EnterIdleState with message: %s", message)
                if message:
                    state_update["conversation"] = [AIMessage(content=message)]
                next_node = f"{snake_case_tool_name}_{current_node_name}"
            elif tool_name == "HandleUserMessage":
                logger.info("Routing to HandleUserMessage")
                next_node = f"{snake_case_tool_name}_{current_node_name}"
            elif tool_name == "StopExecution":
                logger.info("Routing to StopExecution")
                next_node = f"{snake_case_tool_name}_{current_node_name}"
            elif tool_name == "MoveToNextNode":
                logger.info("Routing to MoveToNextNode")
                next_node = "subgraph_router"
    else:
        # Route to generic tool node for non-interrupt tools
        logger.info(f"Routing to generic tool node for {tool_name}")
        next_node = f"generic_tool_node_{current_node_name}"

    return state_update, next_node


def log_llm_response(response):
    logger.info("LLM Response:")
    if hasattr(response, "content") and response.content:
        logger.info(f"  Content: {response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        logger.info(f"  Tool calls: {response.tool_calls}")


def generate_recovery_message(error_description: str) -> str:
    """
    Generate a recovery message for error situations.

    Args:
        error_description: Description of the error that occurred

    Returns:
        A formatted recovery message string
    """
    recovery_message = f"{error_description} "
    recovery_message += f"I will generate relevant and helpful content based on the provided instructions. "
    recovery_message += "Now I will continue the execution."
    return recovery_message


def validate_and_handle_empty_response(response: Any) -> Any:
    """
    Validate LLM response and handle empty responses by creating a self-recovery message.

    Args:
        response: The LLM response to validate

    Returns:
        The original response if valid, or a new AIMessage with recovery content
    """
    # Check if response is None or doesn't have the expected attributes
    if response is None:
        logger.warning("Received None response from LLM")
        recovery_message = generate_recovery_message("I received a None response from the LLM.")
        return AIMessage(content=recovery_message)

    # Check if response has no content and no tool calls (empty response)
    has_content = False
    if hasattr(response, "content") and response.content:
        if isinstance(response.content, str):
            has_content = response.content.strip() != ""
        elif isinstance(response.content, list):
            has_content = len(response.content) > 0 and any(
                (hasattr(block, 'text') and block.text.strip()) or
                (isinstance(block, dict) and block.get('text', '').strip()) or
                (isinstance(block, str) and block.strip())
                for block in response.content
            )

    has_tool_calls = hasattr(response, "tool_calls") and response.tool_calls

    if not has_content and not has_tool_calls:
        logger.warning("LLM generated an empty response with no content and no tool calls")
        recovery_message = generate_recovery_message("I generated an empty response and no tool calls.")
        return AIMessage(content=recovery_message)

    # Response is valid, return as-is
    return response


def new_node_agent(current_node: dict, node_edges: list) -> Callable:
    """
    Create a new agent with the given prompt and tools.

    Args:
        current_node: The current node information
        node_edges: The edges for the current node

    Returns:
        A callable function that processes the state
    """
    # Get node type, default to "DefaultNode" if not specified
    node_type = current_node.get("type", "DefaultNode")
    node_name = current_node.get("name", "unknown_name")

    # Get the node type instance from the registry
    node_type_instance = node_type_registry.create(node_type)

    async def execute_node_action(state: State, config: RunnableConfig):
        """
        Execute the action for the current node using the node type's execute method.

        Args:
            state: The current state
            config: The runnable configuration

        Returns:
            The result of the node execution
        """
        logger.info(f"Executing action for node: {current_node['name']} of type: {node_type}")

        try:
            # Get LLM configuration from config if available
            llm_config = config.get("configurable", {}).get("llm_config")
            provider = llm_config.get("provider_name", "") if llm_config else ""

            # Initialize LLM based on configuration
            try:
                llm_without_tools = initialize_llm(llm_config)
            except Exception as e:
                error_message = f"Error initializing LLM: {str(e)}"
                logger.error(error_message)
                recovery_message = generate_recovery_message(f"I encountered an error while initializing the LLM: {error_message}.")
                return AIMessage(content=recovery_message)

            # Generate tools for this node using the tool generator
            node_tools = await generate_tools_for_node(
                node_type=node_type,
                node_name=node_name,
                node_config=current_node,
                provider=provider
            )

            # Bind tools to LLM
            llm = llm_without_tools.bind_tools(node_tools["formatted"])

            # Optimize history for the specific provider
            optimized_history = optimize_messages_for_provider(
                state.get("full_history", []), provider
            )

            # Create a new modified state with the optimized history
            optimized_state = {**state, "full_history": optimized_history}

            # Use the node type's execute method with the optimized state
            response = await node_type_instance.execute(
                state=optimized_state,
                node_config=current_node,
                node_edges=node_edges,
                llm=llm,
                llm_without_tools=llm_without_tools,
                config=config,
            )

            # Validate and handle empty responses
            response = validate_and_handle_empty_response(response)

            # Log token usage if available
            if hasattr(response, "usage_metadata") and response.usage_metadata:
                logger.info(f"Token usage: {response.usage_metadata}")
                input_details = response.usage_metadata.get("input_token_details")
                if input_details:
                    logger.info(
                        f"  Input details: Cache Read={input_details.get('cache_read', 'N/A')}, "
                        f"Cache Creation={input_details.get('cache_creation', 'N/A')}"
                    )

            return response

        except Exception as e:
            # Handle any other unexpected errors
            error_message = str(e)
            logger.error(f"Unexpected error during node execution: {error_message}")
            raise e

    async def node_fn(state: State, config: RunnableConfig):
        thread_id = config.get("configurable", {}).get("thread_id", "unknown_thread")
        logger.info("Executing node: %s of thread %s", current_node["name"], thread_id)

        # 2. Check for pending tool calls and handle them if needed
        pending_tool_call = get_next_pending_tool_call(state["full_history"])

        if pending_tool_call:
            # Use the helper function to determine routing with node type info
            tool_state_update, next_node = await handle_tool_call_routing(
                pending_tool_call,
                current_node["name"],
                node_type,
                node_name,
                current_node
            )
            if next_node:
                return Command(update=tool_state_update, goto=next_node)

        # 3. Handle initial step_prompt if current_node is not set
        if not state.get("current_node"):
            step_prompt = node_type_instance.generate_step_prompt(current_node, node_edges)

            return Command(
                update={
                    "current_node": current_node,
                    "full_history": [AIMessage(content=step_prompt)]
                },
                goto=current_node["name"],
            )

        # 4. Process any pending interrupts from Redis queue
        signals = check_for_interrupt_signal(thread_id)

        # Handle stop signal with priority
        if signals["stop"]:
            logger.info(f"Stop signal detected for thread {thread_id}, injecting StopExecution tool")
            modified_state, signal_updates = inject_stop_execution_tool(state)
            return Command(update=signal_updates, goto=current_node["name"])

        # Handle new message signal
        if signals["new_message"]:
            logger.info(f"New message signal detected for thread {thread_id}, injecting HandleUserMessage tool")
            modified_state, signal_updates = inject_handle_user_message_tool(state)
            return Command(update=signal_updates, goto=current_node["name"])

        # 5. Execute node action using the potentially modified state
        response = await execute_node_action(state, config)

        # 6. Check for interrupt signals again after node execution
        pending_tool_call = get_next_pending_tool_call(state["full_history"])
        if not pending_tool_call:
            signals = check_for_interrupt_signal(thread_id)

            # Handle stop signal with priority
            if signals["stop"]:
                logger.info(f"Stop signal detected after node execution for thread {thread_id}, injecting StopExecution tool")
                modified_state, signal_updates = inject_stop_execution_tool(state)
                return Command(update=signal_updates, goto=current_node["name"])

            # Handle new message signal
            if signals["new_message"]:
                logger.info(f"New message signal detected after node execution for thread {thread_id}, injecting HandleUserMessage tool")
                modified_state, signal_updates = inject_handle_user_message_tool(state)
                return Command(update=signal_updates, goto=current_node["name"])

        return Command(update={"full_history": [response]}, goto=current_node["name"])

    return node_fn
