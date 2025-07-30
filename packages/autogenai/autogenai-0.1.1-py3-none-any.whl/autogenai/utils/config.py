import os
from dotenv import load_dotenv

load_dotenv()

def get_env(key: str, default=None, required: bool = False):
    value = os.getenv(key, default)
    if required and value is None:
        raise EnvironmentError(f"Missing required environment variable: {key}")
    return value

DEFAULT_MODELS = {
    "openai": get_env("DEFAULT_OPENAI_MODEL", default="gpt-3.5-turbo"),
    "gemini": get_env("DEFAULT_GEMINI_MODEL", default="models/gemini-1.5-flash")
}
