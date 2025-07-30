from autogenai.core.factory import LLMFactory

engine = LLMFactory.create(engine_name="gemini", model="models/gemini-1.5-flash")
response = engine.chat("What is the meaning of software craftsmanship?")
print(response)
