import os
import chainlit as cl
import httpx
from typing import Dict

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

async def query_backend(query: str) -> Dict:
    """Send query to FastAPI backend and return response."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{BACKEND_URL}/assistant/query",
                json={"query": query}
            )
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        raise ConnectionError("Backend service is not responding. Please try again later.")
    except httpx.HTTPStatusError as e:
        raise ConnectionError(f"Backend service error: {e.response.status_code}")
    except httpx.RequestError:
        raise ConnectionError("Cannot connect to backend service.")

async def populate_knowledge() -> Dict:
    """Populate the knowledge base from the backend."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{BACKEND_URL}/assistant/populate-knowledge")
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        raise ConnectionError("Knowledge population timed out. This operation might take longer than expected.")
    except httpx.HTTPStatusError as e:
        raise ConnectionError(f"Failed to populate knowledge: {e.response.status_code}")
    except httpx.RequestError:
        raise ConnectionError("Cannot connect to backend service for knowledge population.")

@cl.on_chat_start
async def start_chat():
    """Initialize the chat session."""
    actions = [
        cl.Action(
            name="populate_knowledge",
            label="Populate Knowledge Base",
            description="Load or reload the vitamin knowledge base",
            payload={}  # Added required payload field
        )
    ]
    await cl.Message(
        content="Hello! I'm your RAG Assistant. How can I help you learn about vitamins today?",
        actions=actions
    ).send()

@cl.action_callback("populate_knowledge")
async def on_populate(action):
    """Handle knowledge population request."""
    await cl.Message(content="🔄 Populating knowledge base... Please wait.").send()
    try:
        response = await populate_knowledge()
        await cl.Message(content="✅ Knowledge base successfully populated!").send()
    except ConnectionError as e:
        await cl.Message(content=f"❌ {str(e)}").send()
    except Exception:
        await cl.Message(content="❌ Failed to populate knowledge base.").send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming chat messages."""
    try:
        response = await query_backend(message.content)
        await cl.Message(content=response["response"]).send()
    except ConnectionError as e:
        await cl.Message(content=f"🔌 Connection Error: {str(e)}").send()
    except KeyError:
        await cl.Message(content="⚠️ Invalid response format from backend service.").send()
    except Exception:
        await cl.Message(content="🚨 An unexpected error occurred. Please try again later.").send()
