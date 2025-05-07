from openai import OpenAI
from typing import List

from backend.models.client import get_openai_client

def embed_text(text: str, model: str = "text-embedding-ada-002") -> List[float]:
  """
  Generate an embedding vector for a single input string.
  """
  client = get_openai_client()
  resp = client.embeddings.create(
    model=model,
    input=text,
    encoding_format="float"
  )
  return resp.data[0].embedding

def embed_texts(texts: List[str], model: str = "text-embedding-ada-002") -> List[List[float]]:
  """
  Generate embedding vectors for a list of input strings in bulk.
  """
  client = get_openai_client()
  resp = client.embeddings.create(
    model=model,
    input=texts,
    encoding_format="float"
  )
  return [d.embedding for d in resp.data]
