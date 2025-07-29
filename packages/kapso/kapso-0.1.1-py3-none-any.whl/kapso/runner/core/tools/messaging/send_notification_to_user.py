"""
Definition for the send_notification_to_user tool.
"""

import logging

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from kapso.runner.channels.models import ChannelMessage, MessageChannelType, MessageContentType
from kapso.runner.channels.factory import send_message

logger = logging.getLogger(__name__)


@tool
async def send_notification_to_user(message: str, config: RunnableConfig) -> str:
    """
    Use this function ONLY to send notifications, updates, confirmations, or messages to the user when NO response or input is expected.
    The message MUST NOT end with a question mark and should clearly indicate that no reply is needed.
    NEVER use this function when user input or interaction is required.

    Guidelines:
    - Use for clear, concise statements. Do not include questions, prompts or requests for information or feedback.
    - Ensure the message adheres to messaging platform formatting rules.
    - This tool continues execution immediately after sending the message.

    Example Usage:
      - "Your appointment has been confirmed for tomorrow at 2 PM."
      - "I have completed processing your request."
      - "Here is the structure for the new report. Feel free to review it later."

    Args:
        message (str): A clear and concise statement informing the user. Must NOT be a question or imply that user feedback or a reply is expected.

    Returns:
        str: Confirmation that the message was sent successfully.
    """
    # All channel-specific details come from configurable
    configurable = config.get("configurable", {})
    recipient_id = configurable.get("phone_number")
    thread_id = configurable.get("thread_id")
    test_mode = configurable.get("test_mode", False)
    # Get channel type from configurable if present, default to whatsapp
    channel_type = configurable.get("channel_type", "whatsapp")
    
    # Create channel message
    channel_message = ChannelMessage(
        content=message,
        channel_type=MessageChannelType(channel_type),
        recipient_id=recipient_id,
        thread_id=thread_id,
        content_type=MessageContentType.TEXT,
        metadata={"test_mode": test_mode}
    )
    if test_mode:
        return f"Message sent: {message}"
    else:
        # Send directly via factory function
        return await send_message(channel_message)
