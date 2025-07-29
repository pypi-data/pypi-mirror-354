"""
Base runner for all specialized runner implementations.
"""

import logging
import json
from typing import Dict, Any, Optional

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.types import Command
from langgraph.types import StateSnapshot

from kapso.runner.core.persistence import create_checkpointer
from kapso.runner.core.graph_builder import GraphBuilder
from kapso.runner.utils.message_utils import recursively_convert_messages_to_openai_format
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

# Create a logger for this module
logger = logging.getLogger(__name__)

class BaseRunner:
    """
    Base class providing common functionality for all specialized runners.

    This class contains shared logic for graph building, checkpointing, and
    state management.
    """

    def __init__(self, debug: bool = False):
        if debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

    async def initialize(self, checkpointer: AsyncPostgresSaver | None = None):
        """Initialize the runner with PostgreSQL checkpointer."""
        self.checkpointer = checkpointer or await create_checkpointer()
        self.graph_builder = GraphBuilder(checkpointer=self.checkpointer)
        logger.info("Runner initialized with PostgreSQL checkpointer")

    def run(self, graph_definition: Dict[str, Any], thread_id: Optional[str] = None, message_input: Optional[Dict[str, Any]] = None, is_new_conversation: bool = False, phone_number: Optional[str] = None, test_mode: bool = False, agent_prompt: Optional[str] = None, llm_config: Optional[Dict[str, Any]] = None, last_interrupt_tool_call_id: Optional[str] = None) -> Dict[str, Any]:
        """Run the runner with the given parameters."""
        pass

    def stream(self, graph_definition: Dict[str, Any], thread_id: Optional[str] = None, message_input: Optional[Dict[str, Any]] = None, is_new_conversation: bool = False, phone_number: Optional[str] = None, test_mode: bool = False, agent_prompt: Optional[str] = None, llm_config: Optional[Dict[str, Any]] = None, last_interrupt_tool_call_id: Optional[str] = None) -> Dict[str, Any]:
        """Stream the runner with the given parameters."""
        pass

    def _prepare_config(
        self,
        graph_definition: Dict,
        thread_id: str,
        test_mode: bool,
        agent_prompt: Optional[str],
        contact_information: Optional[Dict[str, Any]] = None,
        llm_config: Optional[Dict[str, Any]] = None,
        last_interrupt_tool_call_id: Optional[str] = None,
        channel_config: Optional[Dict[str, Any]] = None,
        phone_number: Optional[str] = None,  # For backward compatibility
    ) -> Dict[str, Any]:
        """
        Prepare the configuration for graph execution.

        Args:
            graph_definition: The graph definition dictionary
            thread_id: Thread ID for the conversation
            test_mode: Flag indicating if test mode is enabled
            agent_prompt: Optional agent prompt
            contact_information: Optional contact information (phone, name, metadata)
            llm_config: Optional LLM configuration
            last_interrupt_tool_call_id: Optional ID of the interrupt tool call we're resuming
            channel_config: Optional channel configuration
            phone_number: Optional phone number (deprecated, use contact_information)

        Returns:
            Dict[str, Any]: The prepared configuration
        """
        # If phone_number is provided but contact_information is not, create contact_information
        if phone_number is not None and contact_information is None:
            contact_information = {"phone_number": phone_number}
        # If contact_information is provided, extract phone_number for backward compatibility
        elif contact_information is not None and "phone_number" in contact_information:
            phone_number = contact_information["phone_number"]

        config = {
            "configurable": {
                "thread_id": thread_id,
                "test_mode": test_mode,
                "contact_information": contact_information,  # Add contact_information
                "phone_number": phone_number,  # Keep for backward compatibility
                "nodes_by_name": self.graph_builder.nodes_by_name(graph_definition),
                "node_edges": self.graph_builder.node_edges(graph_definition),
                "llm_config": llm_config or {},
            },
            "recursion_limit": 80,
        }

        if last_interrupt_tool_call_id:
            config["configurable"]["resume_tool_call_id"] = last_interrupt_tool_call_id

        # Add agent prompt if provided
        if agent_prompt:
            config["configurable"]["agent_prompt"] = agent_prompt

        # Add channel_type if provided in channel_config
        if channel_config and "type" in channel_config:
            config["configurable"]["channel_type"] = channel_config.get("type")

        return config

    def _get_thread_id(self, thread_id: Optional[str]) -> str:
        """Generate a thread ID if not provided."""
        if not thread_id:
            import uuid
            new_thread_id = str(uuid.uuid4())
            logger.info(f"Generated new thread ID: {new_thread_id}")
            return new_thread_id
        return thread_id

    def _prepare_input_state(self, is_new_conversation: bool, message_input: Optional[Dict[str, Any]]) -> Any:
        """
        Prepare the input state based on whether this is a new conversation and the message payload structure.

        Args:
            is_new_conversation: Flag indicating if this is a new conversation
            message_input: Optional message payload as a dictionary

        Returns:
            Either a Command to resume the conversation or an initial state dictionary
        """
        if not is_new_conversation:
            return Command(resume=message_input)

        if message_input is None:
            return Command(resume=None)

        # Extract message components
        msg_type = message_input.get("type")
        msg_content_dict = message_input.get("content", {})

        # Initialize state
        initial_state = {
            "full_history": [],
            "conversation": [],
            "handoff_reason": None,
        }

        if msg_type == "user_input":
            # Handle user-generated content (text for now, multimodal later)
            user_text_for_conv = msg_content_dict.get("text")
            initial_state["conversation"].append(HumanMessage(content=user_text_for_conv))

            # Always add to full_history
            full_history_message = f"This is the start of the AI agent execution. I received the following initial messages from the user: \n<messages>\n{user_text_for_conv}\n</messages>"
            initial_state["full_history"].append(AIMessage(content=full_history_message))

        elif msg_type == "payload":
            # For system payloads, only add to full_history, not to conversation
            initial_state["full_history"].append(
                AIMessage(content=f"System Payload: {json.dumps(msg_content_dict)}")
            )

        else:
            # Unknown message type
            logger.warning(f"Unknown message type: {msg_type}")
            raise ValueError(f"Unknown message type: {msg_type}")

        # Return initial state for new conversations
        return initial_state

    async def cleanup(self):
        """Cleanup resources when shutting down."""
        if hasattr(self, 'checkpointer') and self.checkpointer and hasattr(self.checkpointer, "pool"):
            logger.info("Closing PostgreSQL connection pool...")
            try:
                await self.checkpointer.pool.close()
                logger.info("PostgreSQL connection pool closed successfully")
            except Exception as e:
                logger.error(f"Error closing PostgreSQL connection pool: {e}")

    def _format_state_response(
        self,
        state: StateSnapshot,
        thread_id: str,
        is_update: bool = False
    ) -> Dict[str, Any]:
        """Format the state response for API consumption, including active interrupts."""

        # Determine overall status
        if is_update:
            status = "running"
        elif not state.next:
            status = "ended"
        else:
            status = "paused"

        # Extract active interrupts using LangGraph property
        active_interrupts = []
        for interrupt in getattr(state, "interrupts", []):
            active_interrupts.append(
                {
                    "id": interrupt.interrupt_id,
                    "value": interrupt.value,
                    "resumable": interrupt.resumable,
                }
            )

        interrupt_tool_call = self._get_interrupt_tool_call(state)

        result = recursively_convert_messages_to_openai_format(
            {
                "status": status,
                "thread_id": thread_id,
                "state": {
                    "values": self._select_message_history_from_state(state.values),
                    "next_nodes": list(state.next),
                    "created_at": state.created_at,
                },
                "current_node": self._select_current_node_from_state(state.values),
                "interrupt_tool_call": interrupt_tool_call,  # Keep for backward compatibility
                "active_interrupts": active_interrupts,  # Add new interrupt information
                "is_update": is_update,
            }
        )

        return result

    def _select_message_history_from_state(self, state_values: Dict[str, Any]) -> Dict[str, Any]:
        """Extract message history from state values."""
        return {
            key: value
            for key, value in state_values.items()
            if key in ["full_history", "conversation"]
        }

    def _select_current_node_from_state(self, state_values: Dict[str, Any]) -> Dict[str, Any]:
        """Extract current node information from state values."""
        current_node = state_values.get("current_node", {})

        # Remove knowledge_base_text from current_node
        current_node = {
            key: value for key, value in current_node.items() if key != "knowledge_base"
        }

        # If global, replace name with original_name
        if current_node.get("global") and current_node.get("original_name"):
            current_node["name"] = current_node.get("original_name")

        return current_node

    def _get_interrupt_tool_call(self, state: StateSnapshot) -> Optional[Dict[str, Any]]:
        """Extract interrupt tool call from state, if any."""
        tasks = state.tasks
        if not tasks or len(tasks) == 0:
            return None

        task = tasks[0]
        interrupts = task.interrupts
        if not interrupts or len(interrupts) == 0:
            return None

        return interrupts[0].value.get("tool_call")