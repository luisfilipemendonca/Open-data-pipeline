import os

from ollama import AsyncClient

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")

client = AsyncClient(host=OLLAMA_HOST)


async def generate_response(
    messages: list[dict[str, str]], response_schema: dict
) -> str:
    response = await client.chat(
        model=OLLAMA_MODEL,
        messages=messages,
        format=response_schema,
        options={"temperature": 0},
        think=False,
    )

    return response.message.content or ""
