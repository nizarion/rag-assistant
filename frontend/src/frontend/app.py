import os
import chainlit as cl
import httpx
from typing import Dict
from frontend.prompts import UIPrompts, ActionLabels

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
prompts = UIPrompts()
actions = ActionLabels()

async def call_backend(endpoint: str, timeout: float = 10.0, **kwargs) -> Dict:
    """Generic backend API call with error handling."""
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(f"{BACKEND_URL}/assistant/{endpoint}", **kwargs)
            response.raise_for_status()
            return response.json()
    except (httpx.TimeoutException, httpx.RequestError, httpx.HTTPStatusError) as e:
        raise ConnectionError(f"Backend service error: {str(e)}")

@cl.on_chat_start
async def start_chat():
    """Initialize chat session with knowledge base action."""
    await cl.Message(
        content=prompts.welcome,
        actions=[
            cl.Action(
                name="populate_knowledge",
                label=actions.populate_kb_label,
                description=actions.populate_kb_desc,
                payload={}
            )
        ]
    ).send()

@cl.action_callback("populate_knowledge")
async def on_populate(action):
    """Handle knowledge population request."""
    try:
        await call_backend("populate-knowledge", timeout=30.0)
        await cl.Message(content=prompts.kb_populated).send()
    except Exception as e:
        await cl.Message(content=f"{prompts.error_prefix} {str(e)}").send()

@cl.on_message
async def main(message: cl.Message):
    """Handle chat messages."""
    try:
        response = await call_backend("query", json={"query": message.content})
        await cl.Message(content=response["response"]).send()
    except Exception as e:
        await cl.Message(content=f"{prompts.error_prefix} {str(e)}").send()
