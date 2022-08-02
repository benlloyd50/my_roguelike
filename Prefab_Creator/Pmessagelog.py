from collections import deque

class MessageLog:
    """ Logs `5` of the most recent messages
        *Does not currently keep old messages
    """
    def __init__(self, maxlen: int = 5):
        self.messages = deque(maxlen=maxlen)

    def add(self, message: str):
        """Add new message to log"""
        self.messages.appendleft(message)

    @property
    def recent(self) -> list:
        """Get `5` of most recent messages"""
        return [msg for msg in reversed(self.messages)]