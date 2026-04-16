# llama-stack + Infinispan vector IO demo

This repository is a minimal demo showing how to use **Infinispan 16.1** as the **vector IO backend** for **llama-stack**.

It provides two Python examples:

- **No RAG**: send a prompt through llama-stack and get a model response
- **RAG**: upload a local document, store its embeddings in Infinispan, and query it with file search

The RAG example introduces supplementary knowledge concerning the Pataphysical science of **Chelonofelodynamics**, a field residing comfortably beyond current epistemological boundaries and, in all likelihood, beyond the representational reach of LLM.

## Requirements

Install the following beforehand:

- **Python 3.12+**
- **Docker** with Docker Compose support

The rest of the demo dependencies are provided by the repository:

- **Ollama** runs in a container and serves `llama3.2:3b`
- **Infinispan 16.1** runs in a container
- **llama-stack** runs locally through `uv`

Default endpoints used by this demo:

- llama-stack: `http://localhost:8321`
- Ollama: `http://localhost:11434`
- Infinispan: `http://localhost:11222`

Default Infinispan credentials used by the distro:

- username: `admin`
- password: `password`

## Setup

### Option 1: Use containerized Ollama (default)

Start both Ollama and Infinispan:

```bash
docker compose up
```

This starts:

- an **Ollama** container on port `11434`
- an **Infinispan 16.1** container on port `11222`

The Ollama container will automatically pull `llama3.2:3b` (this may take several minutes on first run).

> **Note on model selection:** The default `llama3.2:3b` is the smallest model that works well with tool calling in most cases. However, it may occasionally fail with tool-calling errors. For more reliable RAG performance, consider using a larger model like `llama3.1:8b` or `llama3.1:70b`, though these require significantly more disk space and memory.

To use a different model, set the `OLLAMA_MODEL` environment variable:
```bash
OLLAMA_MODEL=llama3.1:8b docker compose up
```

### Option 2: Use your own Ollama installation (faster)

If you already have Ollama running locally on port `11434`, start only Infinispan:

```bash
docker compose up infinispan
```

Make sure your local Ollama has the model available (default is `llama3.2:3b`):
```bash
ollama pull llama3.2:3b
```

To use a different model, set the `OLLAMA_MODEL` environment variable when running the Python scripts:
```bash
OLLAMA_MODEL=llama3.1:8b uv run python with-rag.py
```

---

Keep the docker compose process running in one terminal.

## Start llama-stack

In a second terminal, start llama-stack:

```bash
uv run llama stack run distro/infinispan.yaml
```

Keep the llama-stack process running while executing the examples below.

## Run the no-RAG example

In a third terminal, run:

```bash
uv run python without-rag.py
```

This example:

- connects to the local llama-stack OpenAI-compatible endpoint
- sends the question `What is Chelonofelodynamics?`
- prints the model response

## Run the RAG example

With the same services still running, execute:

```bash
uv run python with-rag.py
```

This example:

- uploads `knowledge/chelonofelodynamics_paper.md`
- creates a vector store
- indexes the uploaded file using the Infinispan-backed vector IO provider
- asks the same question using the `file_search` tool
- prints the grounded response

## Configuration notes

The RAG example uses `distro/infinispan.yaml`, which enables:

- the `infinispan` vector IO provider
- the `sentence-transformers` embedding model
- local file storage for uploaded files
- the `file-search` tool runtime

## Advanced Configuration

You can customize the demo using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://localhost:11434` | Ollama endpoint URL |
| `OLLAMA_MODEL` | `llama3.2:3b` | Model to use (both for pulling and inference) |
| `INFINISPAN_URL` | `http://localhost:11222` | Infinispan endpoint URL |
| `INFINISPAN_USERNAME` | `admin` | Infinispan username |
| `INFINISPAN_PASSWORD` | `password` | Infinispan password |

Example using a remote Ollama instance:
```bash
OLLAMA_URL=http://remote-host:11434 uv run llama stack run distro/infinispan.yaml
```