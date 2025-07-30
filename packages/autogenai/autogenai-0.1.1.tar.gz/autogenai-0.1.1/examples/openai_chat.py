from autogenai.core.openai_engine import OpenAIEngine

engine = OpenAIEngine()
response = engine.chat("Tell me a short poem about code.")
print(response)