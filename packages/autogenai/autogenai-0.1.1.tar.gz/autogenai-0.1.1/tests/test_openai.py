import pytest
from unittest.mock import patch
from autogenai.core.openai_engine import OpenAIEngine

@pytest.fixture
def engine(monkeypatch):
    monkeypatch.setenv("OPEN_API_KEY", "dummy")
    return OpenAIEngine()

@patch("autogenai.core.openai_engine.httpx.Client.post")
def test_chat_success(mock_post, engine):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "choices": [{"message": {"content": "Hello world!"}}]
    }

    result = engine.chat("Say hi")
    assert result == "Hello world!"

@patch("autogenai.core.openai_engine.httpx.Client.post")
def test_chat_failure(mock_post, engine):
    mock_post.side_effect = Exception("API down")
    with pytest.raises(Exception) as exc_info:
        engine.chat("Say hi")
    assert "API down" in str(exc_info.value)
