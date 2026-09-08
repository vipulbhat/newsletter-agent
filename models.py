from typing import TypedDict, Literal, Any

class NewsletterState(TypedDict, total=False):
    goal: str
    mode: Literal["autonomous", "hitl"]
    plan: list[str]
    research: list[dict[str, Any]]
    selected_articles: list[dict[str, Any]]
    newsletter: str
    critique: str
    revision_count: int
    approved: bool
    output_path: str
    logs: list[str]
