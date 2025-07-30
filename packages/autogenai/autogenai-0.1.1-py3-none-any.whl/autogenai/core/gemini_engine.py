import google.generativeai as genai
from autogenai.core.base import BaseLLM
from autogenai.utils.logger import get_logger
from autogenai.utils.config import get_env, DEFAULT_MODELS
from autogenai.utils.errors import MissingAPIKeyError

logger = get_logger("GeminiEngine")

class GeminiEngine(BaseLLM):
    def __init__(self, model: str = None):
        try:
            self.api_key = get_env("GEMINI_API_KEY", required=True)
        except EnvironmentError:
            raise MissingAPIKeyError("GEMINI_API_KEY is required but not set.")
        self.model = model or DEFAULT_MODELS["gemini"]
        genai.configure(api_key=self.api_key)
        self.chat_model = genai.GenerativeModel(model)
        logger.info(f"GeminiEngine initialized with model: {model}")

    def chat(self, prompt: str) -> str:
        try:
            logger.info("Sending Gemini chat request...")
            response = self.chat_model.generate_content(prompt)
            logger.info("Gemini response received.")
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini chat error: {e}")
            raise RuntimeError("Gemini API call failed") from e

    def summarize(self, text: str) -> str:
        prompt = f"Summarize the following text:\n\n{text}"
        return self.chat(prompt)