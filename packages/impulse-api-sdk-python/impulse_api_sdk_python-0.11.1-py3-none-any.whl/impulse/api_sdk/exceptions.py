from typing import Any, Optional


class ImpulseClientError(Exception):
    """
    Exception raised when attempting to send an invalid value to the Impulse API.
    """
    pass


class ImpulseServerError(Exception):
    """Exception raised for errors returned by the Impulse API."""

    def __init__(self, status: int, message: str, details: Optional[Any] = None):
        """
        Initialize the ImpulseAPIError.

        Args:
            status (int): The HTTP status code of the error.
            message (str): The error message.
            details (Optional[Any]): Additional error details, if any.
        """
        self.status = status
        self.details = details
        super().__init__(f"Impulse API Error (Status {status}): {message}")
