from fastapi import APIRouter
from pydantic import BaseModel
from backend.core.assistant import retrieve_relevant_passages
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/assistant")

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
async def query_assistant(request: QueryRequest):
    passages = retrieve_relevant_passages(request.query)
    prompt = "\n".join(passages) + f"\n\nQuestion: {request.query}\nAnswer:"

    response = client.chat.completions.create(
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        messages=[{"role": "user", "content": prompt}]
    )

    return {"response": response.choices[0].message.content}