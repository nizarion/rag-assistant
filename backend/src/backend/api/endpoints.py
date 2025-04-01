from fastapi import APIRouter
from pydantic import BaseModel
from backend.core.assistant import (
    retrieve_relevant_passages,
    get_embedding,
    vector_store,
)
from backend.core.logging_config import setup_logger
from backend.core.azure_client import chat_client
import os
from dotenv import load_dotenv

_ = load_dotenv()

logger = setup_logger(__name__)

router = APIRouter(prefix="/assistant")


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
    system_prompt += "\n".join(passages)
    logger.info(f"System prompt: {system_prompt}")

    response = chat_client.chat.completions.create(
        model=os.getenv("MODEL_DEPLOYMENT_NAME") or "changeme",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.query},
        ],
    )

    return {"response": response.choices[0].message.content}


@router.post("/populate-knowledge")
async def populate_data():
    """Populate vector store with vitamin knowledge data."""
    logger.info("Starting to populate vitamin knowledge data")

    passages = [
        "Vitamin C is essential for the growth and repair of tissues in the body.",
        "Vitamin D is important for maintaining healthy bones and teeth. ",
        "Vitamin E is a powerful antioxidant that helps protect cells from damage.",
        "Vitamin K is crucial for blood clotting and bone health.",
        "Vitamin A is important for vision, immune function, and skin health.",
        "B vitamins play a vital role in energy production and the formation of red blood cells.",
        "Vitamin B12 is essential for nerve function and the production of DNA and red blood cells.",
        "Folic acid is important for cell division and the formation of DNA.",
        "Vitamin B6 is involved in protein metabolism and cognitive development.",
        "Vitamin B1 (thiamine) is important for energy metabolism and nerve function.",
        "Vitamin B2 (riboflavin) is important for energy production and cellular function.",
        "Vitamin B3 (niacin) is important for energy metabolism and DNA repair.",
        "Vitamin B5 (pantothenic acid) is important for the synthesis of coenzyme A.",
        "Vitamin B7 (biotin) is important for carbohydrate and fat metabolism.",
        "Vitamin B9 (folate) is important for DNA synthesis and repair.",
        "Vitamin C is important for collagen synthesis and immune function.",
        "Vitamin D is important for calcium absorption and bone health.",
        "Vitamin E is important for skin health and immune function.",
        "Vitamin K is important for blood clotting and bone metabolism.",
        "Vitamin A is important for vision and immune function.",
        "Vitamin B12 is important for nerve function and DNA synthesis.",
        "Vitamin B6 is important for protein metabolism and cognitive function.",
        "Vitamin B1 is important for energy metabolism and nerve function.",
        "Vitamin B2 is important for energy production and cellular function.",
        "Vitamin B3 is important for energy metabolism and DNA repair.",
        "Vitamin B5 is important for the synthesis of coenzyme A.",
        "Vitamin B7 is important for carbohydrate and fat metabolism.",
        "Vitamin B9 is important for DNA synthesis and repair.",
    ]

    try:
        # Get embeddings for each passage in batches
        logger.info(f"Generating embeddings for {len(passages)} passages")
        embeddings: list[list[float]] = []
        batch_size = 10

        for i in range(0, len(passages), batch_size):
            batch = passages[i : i + batch_size]
            batch_embeddings = [get_embedding(passage) for passage in batch]

            # Validate embeddings
            if any(not embedding for embedding in batch_embeddings):
                raise ValueError(
                    "Failed to generate valid embeddings for some passages"
                )

            embeddings.extend(batch_embeddings)
            logger.debug(f"Processed {i + len(batch)}/{len(passages)} passages")

        # Store passages and their embeddings
        logger.info("Storing passages and embeddings in vector store")
        vector_store.store_passages(passages, embeddings)

        logger.info("Successfully populated vitamin knowledge data")
        return {
            "status": "success",
            "message": "Vitamin knowledge has been stored in the vector database",
            "count": len(passages),
        }
    except Exception as e:
        logger.error(f"Error populating vitamin knowledge: {str(e)}")
        return {
            "status": "error",
            "message": f"Failed to store vitamin knowledge: {str(e)}",
        }


@router.post("/ping")
async def ping():
    """Ping the assistant API to check if it's alive."""
    return {"status": "success", "message": "Assistant API is healthy."}
