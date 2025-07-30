import sys
from autogenai import tools

prompt = " ".join(sys.argv[1:])
if not prompt:
    print("Usage: python sdk_cli.py <your prompt>")
    sys.exit(1)

response = tools.chat(prompt, engine_name="gemini", model="models/gemini-1.5-flash")
print(response)
