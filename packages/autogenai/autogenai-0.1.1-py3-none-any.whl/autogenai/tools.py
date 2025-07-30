from autogenai.core.factory import LLMFactory

def chat(prompt: str, engine_name:str = None, model: str = None):
    engine = LLMFactory.create(engine_name, model=model)
    return engine.chat(prompt)

def summarize(text: str, engine_name: str = None, model: str = None):
    engine = LLMFactory.create(engine_name, model=model)
    return engine.summarize(text)

def summaize_batch(texts: list[str], engine_name: str = None, model: str = None) -> list[str]:
    engine = LLMFactory.create(engine_name, model=model)
    return [engine.summarize(text) for text in texts]
