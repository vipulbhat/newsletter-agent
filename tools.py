import os
from tavily import TavilyClient

def web_search(query: str, max_results: int = 10) -> list[dict]:
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    result = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        include_answer=False,
    )
    return result.get("results", [])

def extract_articles(results: list[dict]) -> list[dict]:
    articles = []
    for r in results:
        articles.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "content": r.get("content", ""),
            "source": r.get("url", "").split("/")[2] if r.get("url") else "",
            "score": r.get("score", 0),
        })
    return articles
