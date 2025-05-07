# data/search/faq.py

import os
from typing import List

import openai
import typesense
from pydantic import BaseModel

# Load environment variables for API keys
TYPESENSE_API_KEY = os.getenv("TYPESENSE_API_KEY")
TYPESENSE_HOST = os.getenv("TYPESENSE_HOST", "localhost")
TYPESENSE_PORT = os.getenv("TYPESENSE_PORT", "8108")
TYPESENSE_PROTOCOL = os.getenv("TYPESENSE_PROTOCOL", "http")

# Initialize OpenAI and Typesense clients
openai.api_key = os.getenv("OPENAI_API_KEY")

typesense_client = typesense.Client({
    "api_key": TYPESENSE_API_KEY,
    "nodes": [{
        "host": TYPESENSE_HOST,
        "port": TYPESENSE_PORT,
        "protocol": TYPESENSE_PROTOCOL
    }],
    "connection_timeout_seconds": 2
})

class FaqItem(BaseModel):
    question: str
    answer: str


def _ensure_faq_collection():
    """
    Create the 'faqs' collection in Typesense if it doesn't already exist.
    The collection uses a vector field for the question embeddings.
    """
    try:
        typesense_client.collections["faqs"].retrieve()
    except Exception:
        schema = {
            "name": "faqs",
            "fields": [
                {"name": "question", "type": "string"},
                {"name": "answer", "type": "string"},
                {"name": "question_vector", "type": "float[]", "num_dim": 1536, "index": True}
            ],
            "default_sorting_field": "question"
        }
        typesense_client.collections.create(schema)


def add_faq_entries_to_typesense(faq_items: List[FaqItem]):
    """
    Adds a list of FAQ items to the Typesense vector collection.
    For each question, it generates an OpenAI embedding and stores it in the 'question_vector' field.
    """
    _ensure_faq_collection()
    for item in faq_items:
        # Generate embedding for the question
        resp = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=item.question
        )
        embedding = resp["data"][0]["embedding"]

        # Create document payload
        doc = {
            "question": item.question,
            "answer": item.answer,
            "question_vector": embedding
        }
        # Index document into Typesense
        typesense_client.collections["faqs"].documents.create(doc)
