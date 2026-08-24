import os
from langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import logging


# configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


load_dotenv()


@tool
def search_web(topic: str) -> str:
    """Search the web for a given topic and return the results."""
    logging.info(f"Searching the web for topic: {topic}")
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    return tavily_client.search(topic)

