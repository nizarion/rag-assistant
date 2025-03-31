from fastapi import APIRouter
from pydantic import BaseModel
from backend.core.assistant import retrieve_relevant_passages, get_embedding, vector_store
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

@router.post("/populate-jokes")
async def populate_joke_data():
    joke_passages = [
        "Zeus, Poseidon, and Hades walk into a bar. Zeus orders a lightning bolt cocktail, Poseidon asks for a sea breeze, and Hades just wants a Death by Chocolate.",
        "Why don't Greek gods use social media? Because they have too much drama in their lives already!",
        "Hercules is known for his twelve labors and incredible strength. He's basically the original gym influencer.",
        "Apollo is the god of music, poetry, and the sun. He's basically the original multi-tasking freelancer.",
        "Athena is the goddess of wisdom and strategic warfare. She's like a CEO who also knows martial arts.",
    ]
    
    # Get embeddings for each passage
    embeddings = [get_embedding(passage) for passage in joke_passages]
    
    # Store passages and their embeddings
    vector_store.store_passages(joke_passages, embeddings)
    
    return {"status": "success", "message": "Joke passages have been stored in the vector database"}

@router.post("/ping")
async def ping():
    """Ping the assistant API to check if it's alive."""
    return {"status": "success", "message": "Assistant API is alive."}