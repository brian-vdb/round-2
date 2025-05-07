# data/search/faq.py

from openai import OpenAI
from pydantic import BaseModel

class FaqItem(BaseModel):
  question: str
  answer: str

