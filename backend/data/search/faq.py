# data/search/faq.py

import os
from pydantic import BaseModel
from typing import List
from pymongo.operations import SearchIndexModel

from models.embedding import embed_text, embed_texts
from data.search.client import get_mongo_client

class FaqItem(BaseModel):
  question: str
  answer: str

def get_faqs_collection():
  """
  Returns the MongoDB collection for FAQs, using MONGO_DB env or default 'round-2'.
  """
  client = get_mongo_client()
  db_name = os.getenv("MONGO_DB", "round-2")
  return client[db_name]["faqs"]

def add_faq_entries_to_mongo(faq_items: List[FaqItem]):
  """
  Adds FAQ items to MongoDB 'faqs' collection with OpenAI-generated embedding vectors in bulk.
  """
  collection = get_faqs_collection()

  questions = [item.question for item in faq_items]
  vectors = embed_texts(questions)

  docs = []
  for item, vec in zip(faq_items, vectors):
    docs.append({
      "question": item.question,
      "answer": item.answer,
      "question_vector": vec
    })

  if docs:
    collection.insert_many(docs, ordered=False)

def create_search_index():
  """
  Creates a vector search index on the 'question_vector' field for RAG.
  """
  collection = get_faqs_collection()
  index_model = SearchIndexModel(
    definition={
      "fields": [
        {
          "type": "vector",
          "numDimensions": 1536,
          "path": "question_vector",
          "similarity": "cosine"
        }
      ]
    },
    name="question_vector_index",
    type="vectorSearch"
  )
  try:
    collection.create_search_index(model=index_model)
  except Exception:
    # index may already exist or fail silently
    pass

def initialize_faqs_collection(default_items: List[FaqItem]) -> None:
  """
  Ensure the 'faqs' collection exists, is seeded, and has a vector search index.
  """
  collection = get_faqs_collection()
  if collection.estimated_document_count() == 0:
    add_faq_entries_to_mongo(default_items)
    print(f"[faq.py]: Initialized faq vector database with {len(default_items)} items")
  create_search_index()

def search_faqs(query: str, k: int = 5) -> List[FaqItem]:
  """
  Runs a vectorSearch aggregation against Mongo.
  """
  q_vec = embed_text(query)

  collection = get_faqs_collection()
  pipeline = [
    {
      "$vectorSearch": {
        "index":        "question_vector_index",
        "path":         "question_vector",
        "queryVector":  q_vec,
        "numCandidates": k * 10,
        "limit":        k
      }
    },
    {
      "$project": {
        "question": 1,
        "answer":   1,
        "score":    {"$meta": "vectorSearchScore"}
      }
    }
  ]

  docs = list(collection.aggregate(pipeline))
  return [FaqItem(question=d["question"], answer=d["answer"]) for d in docs]
