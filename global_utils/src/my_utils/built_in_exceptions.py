"""
Built-In and Custom Exceptions.
"""


class InvalidPayloadException(Exception):
    """Exception raised for errors in the input payload from a csv."""

    def __init__(self, payload, message="Please add an Exception Message in utils."):
        self.payload = payload
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}: {self.payload}"
