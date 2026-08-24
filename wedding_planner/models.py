from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

groq_model = init_chat_model("qwen/qwen3.6-27b", model_provider="groq")
