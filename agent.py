from google import genai

#env import
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("api_key")

#step1: autenticate

client = genai.Client(api_key=api_key)

prompt = "what is ai agent in simplet words"

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)

print(response.text)
