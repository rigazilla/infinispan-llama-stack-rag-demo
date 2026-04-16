import os
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8321/v1", api_key="fake")

model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

# Upload a document
file = client.files.create(
    file=open("knowledge/chelonofelodynamics_paper.md", "rb"),
    purpose="assistants",
)

# Create a vector store and index the file
vector_store = client.vector_stores.create(
    name="my-docs",
    file_ids=[file.id],
)

# Ask questions with file search
response = client.responses.create(
    model=f"ollama/{model}",
    input="What is Chelonofelodynamics?",
    tools=[{
        "type": "file_search",
        "vector_store_ids": [vector_store.id],
    }],
)
print(response.output_text)
