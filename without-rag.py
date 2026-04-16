import os
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8321/v1/", api_key="fake")

model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

response = client.responses.create(
    model=f"ollama/{model}",
    input="What is Chelonofelodynamics?",
)
print(response.output_text)
