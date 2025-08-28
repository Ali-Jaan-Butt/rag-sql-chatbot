from groq import Groq
import os
from dotenv import load_dotenv


def api_key():
    load_dotenv()
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return client