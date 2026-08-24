from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

groq_model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")