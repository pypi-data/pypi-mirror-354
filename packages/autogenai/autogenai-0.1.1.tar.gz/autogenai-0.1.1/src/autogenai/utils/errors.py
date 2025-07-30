class LLMEngineError(Exception):
    """Base exception for all LLM engine issues."""

class InvalidEngineError(LLMEngineError):
    """Raised when an unsupported engine is requested."""

class MissingAPIKeyError(LLMEngineError):
    """Raised when a required API key is missing from the .env file."""

class LLMResponseError(LLMEngineError):
    """Raised when an LLM engine returns an unexpected or failed response"""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(message)
