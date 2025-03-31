from fastapi import APIRouter
from pydantic import BaseModel
from backend.core.assistant import retrieve_relevant_passages
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

from logging import getLogger

load_dotenv()

logger = getLogger(__name__)

router = APIRouter(prefix="/assistant")

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


class QueryRequest(BaseModel):
    query: str


@router.post("/query")
async def query_assistant(request: QueryRequest):
    passages = retrieve_relevant_passages(request.query)
    if not passages:
        return {"response": "No relevant passages found."}
    # System prompt for the model
    system_prompt = (
        "You are a helpful assistant that answers questions based on provided passages."
    )
    # Construct the prompt
    # The prompt is a combination of the system prompt and the passages
    # prompt = "\n".join(passages) + f"\n\nQuestion: {request.query}\nAnswer:"
    system_prompt += "\n".join(passages)
    logger.debug(f"System prompt: {system_prompt}")

    response = client.chat.completions.create(
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.query},
        ],
    )

    return {"response": response.choices[0].message.content}
