from autogenai.core.openai_engine import OpenAIEngine
from autogenai.core.gemini_engine import GeminiEngine
from autogenai.utils.logger import get_logger
from autogenai.utils.config import get_env, DEFAULT_MODELS
from autogenai.utils.errors import InvalidEngineError

logger = get_logger("LLMFactory")

class LLMFactory:
    @staticmethod
    def create(engine_name: str = None, model: str = None):
        engine_name = (engine_name or get_env("LLM_ENGINE", default="gemini")).lower()
        selected_model = model or DEFAULT_MODELS.get(engine_name)

        if engine_name == "openai":
            logger.info("Creating OpenAI engine")
            return OpenAIEngine(model=selected_model)
        elif engine_name == "gemini":
            logger.info("Creating Gemini Engine")
            return GeminiEngine(model=selected_model)
        else:
            raise InvalidEngineError(f"Unsupported engine: {engine_name}")
