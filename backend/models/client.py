# models/client.py

from openai import OpenAI

# Initialize and reuse a single OpenAI client instance
def get_openai_client() -> OpenAI:
  """
  Returns a singleton OpenAI client for embeddings and completions.
  """
  return OpenAI()
