"""Back end for using LLM."""

from enum import StrEnum
import os
from typing import Optional

import json
import httpx
from fastapi import FastAPI, HTTPException


app = FastAPI(
    title="Plant Model",
    description="Processes input text to provide watering and fertiliser frequency.",
)

MODEL_NAME = os.getenv("OLLAMA_MODEL")
OLLAMA_URL = "http://ollama:11434/api/chat"


async def invoke_ollama_model(query_text: str) -> dict:
    """Invoke the ollama model with the given text."""
    messages = [
        {
            "role": "system",
            "content": (
                "<Give a prompt to the model>"
            ),
        },
        {"role": "user", "content": query_text},
    ]

    async with httpx.AsyncClient(timeout=httpx.Timeout(60)) as client:
        response = await client.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": False,
                "format": "<select a format for your message>"
            },
        )
        response.raise_for_status()
        content = response.json()["message"]["content"]
        return content


# used gemma3 which seemed to work okay
@app.post("/query")
async def query(query_text: str) -> dict:
    """Extract the plant care info"""
    # Handle bad responses and exceptions
    json_text = json.dumps(query_text, indent=2)
    try:
        result = await invoke_ollama_model(json_text)
        return result
    except (ValueError, httpx.HTTPStatusError) as e:
        raise HTTPException(
            status_code=400, detail={"error": f"Failed to parse model response{e}"}
        )
