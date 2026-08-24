import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def tavily_search(query: str, max_results: int = 5) -> str:
    """Shared Tavily web search wrapper used by all specialized tools."""
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = client.search(query, max_results=max_results)
    formatted = []
    for r in results.get("results", []):
        title = r.get("title", "N/A")
        content = r.get("content", "N/A")
        url = r.get("url", "N/A")
        formatted.append(f"**{title}**\n{content}\nSource: {url}")
    return "\n\n".join(formatted) if formatted else "No results found."
