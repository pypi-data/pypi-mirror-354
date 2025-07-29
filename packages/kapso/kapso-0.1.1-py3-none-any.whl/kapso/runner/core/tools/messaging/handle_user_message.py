"""
Definition for the HandleUserMessage tool.
"""

from pydantic import BaseModel


class HandleUserMessage(BaseModel):
    """
    Internal tool used to handle user message interruptions during agent execution.
    This tool is automatically triggered when a user sends a message while the agent is processing.
    It pauses execution to allow new user messages to be incorporated.
    
    This tool should not be used directly by agents - it's automatically injected when needed.
    """
