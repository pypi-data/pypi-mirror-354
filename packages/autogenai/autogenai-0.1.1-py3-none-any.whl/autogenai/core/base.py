from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """
    Abstract base class for all LLM engines.
    Defines a common interface
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    def chat(self, prompt: str) -> str:
        """Send a chat/completion prompt and return the response"""
        pass

    @abstractmethod
    def achat(self, prompt: str) -> str:
        pass

    @abstractmethod
    def summarize(self, text: str) -> str:
        """Summarize a long text"""
        pass
