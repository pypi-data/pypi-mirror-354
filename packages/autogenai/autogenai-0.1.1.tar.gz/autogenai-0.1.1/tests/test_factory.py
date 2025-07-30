import pytest
from autogenai.core.factory import LLMFactory
from autogenai.core.openai_engine import OpenAIEngine
from autogenai.core.gemini_engine import GeminiEngine
from autogenai.utils.errors import InvalidEngineError

def test_create_openai_engine(monkeypatch):
    monkeypatch.setenv("OPEN_API_KEY", "dummy")
    engine = LLMFactory.create("openai")
    assert isinstance(engine, OpenAIEngine)

def test_create_openai_engine(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy")
    engine = LLMFactory.create("gemini")
    assert isinstance(engine, GeminiEngine)

def test_invalid_engine():
    with pytest.raises(InvalidEngineError):
        LLMFactory.create("unsupported")
