
from functools import lru_cache

import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from langchain.tools import tool

from config import get_required_env


@lru_cache(maxsize=1)
def get_tavily_client():
    """Create and reuse the Tavily client."""
    return TavilyClient(
        api_key=get_required_env("TAVILY_API_KEY")
    )


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic.
    Returns titles, URLs and snippets.
    """
    try:
        tavily = get_tavily_client()

        results = tavily.search(
            query=query,
            max_results=5,
        )

        output = []

        for result in results.get("results", []):
            output.append(
                f"Title: {result.get('title', '')}\n"
                f"URL: {result.get('url', '')}\n"
                f"Snippet: {result.get('content', '')[:300]}\n"
            )

        if not output:
            return "No search results were found."

        return "\n----\n".join(output)

    except Exception as error:
        return f"Web search failed: {str(error)}"


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
        ]):
            tag.decompose()

        content = soup.get_text(
            separator=" ",
            strip=True,
        )

        return content[:5000]

    except Exception as error:
        return f"Could not scrape URL: {str(error)}"


# from langchain.tools import tool 
# import requests
# from bs4 import BeautifulSoup
# from tavily import TavilyClient
# import os 
# from dotenv import load_dotenv
# from rich import print
# load_dotenv()

# tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# @tool
# def web_search(query : str) -> str:
#     """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""
#     results = tavily.search(query=query,max_results=5)
    
#     out = []

#     for r in results['results']:
#         out.append(
#             f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
#         )
    
#     return "\n----\n".join(out)



# @tool
# def scrape_url(url: str) -> str:
#     """Scrape and return clean text content from a given URL for deeper reading."""
#     try:
#         resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
#         soup = BeautifulSoup(resp.text, "html.parser")
#         for tag in soup(["script", "style", "nav", "footer"]):
#             tag.decompose()
#         return soup.get_text(separator=" ", strip=True)[:3000]
#     except Exception as e:
#         return f"Could not scrape URL: {str(e)}"