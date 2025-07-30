"""Exceptions for the OxaPay client."""


class OxaPayError(Exception):
    """Exception raised for OxaPay API errors.

    Attributes:
        code: The error code from the API
        message: The error message from the API

    """

    def __init__(self, code: int, message: str) -> None:
        """Initialize OxaPayError with error code and message.

        Args:
            code: The error code from the API
            message: The error message from the API

        """
        self.code = code
        self.message = message
        super().__init__(f"OxaPay API Error ({code}): {message}")


class OxaPayValidationError(Exception):
    """Exception raised for data validation errors."""
