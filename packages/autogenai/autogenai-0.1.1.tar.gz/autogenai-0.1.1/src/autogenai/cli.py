import argparse
from autogenai.core.factory import LLMFactory

def main():
    parser = argparse.ArgumentParser(description="AutoGenAI CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    chat_parser = subparsers.add_parser("chat", help="Chat with the LLM")
    chat_parser.add_argument("prompt", type=str, help="Prompt to send")
    chat_parser.add_argument("--engine", type=str, default=None, help="LLM engine (e.g., openai, gemini)")
    chat_parser.add_argument("--model", type=str, default=None, help="Model to use")

    args = parser.parse_args()

    if args.command == "chat":
        engine = LLMFactory.create(engine_name=args.engine, model=args.model)
        result = engine.chat(args.prompt)
        print(result)
