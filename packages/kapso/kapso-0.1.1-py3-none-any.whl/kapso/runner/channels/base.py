from abc import ABC, abstractmethod
from typing import Dict, Any

from kapso.runner.channels.models import ChannelMessage

class BaseChannelAdapter(ABC):
    """Base class for all channel adapters."""

    @abstractmethod
    async def send_message(self, message: ChannelMessage) -> str:
        """
        Send any type of message through this channel.

        The adapter will handle different content types internally.

        Args:
            message: The channel-agnostic message to send

        Returns:
            A string indicating success or failure
        """
        pass

    @classmethod
    @abstractmethod
    def from_config(cls, config: Dict[str, Any]) -> 'BaseChannelAdapter':
        """Create an adapter instance from a configuration dict."""
        pass