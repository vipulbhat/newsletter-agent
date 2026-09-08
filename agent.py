import json
import os
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

from models import NewsletterState
from prompts import PLANNER, SELECTOR, WRITER, CRITIC, REVISER
from tools import web_search, extract_articles

load_dotenv()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
llm = ChatOpenAI(model=MODEL, temperature=0.2)

def text(messages):
    return llm.invoke(messages).content

def plan_node(state: NewsletterState):
    plan = text([SystemMessage(content=PLANNER), HumanMessage(content=state["goal"])])
    return {"plan": [x.strip() for x in plan.splitlines() if x.strip()], "logs": state.get("logs", []) + ["Planner completed"]}

def research_node(state: NewsletterState):
    results = extract_articles(web_search(f"latest AI agent news {state['goal']}", 12))
    return {"research": results, "logs": state.get("logs", []) + [f"Web research completed: {len(results)} results"]}

def select_node(state: NewsletterState):
    raw = text([SystemMessage(content=SELECTOR), HumanMessage(content=json.dumps(state["research"], ensure_ascii=False))])
    try:
        selected = json.loads(raw).get("articles", [])
    except json.JSONDecodeError:
        selected = state["research"][:7]
    return {"selected_articles": selected[:7], "logs": state.get("logs", []) + [f"Selected {len(selected[:7])} articles"]}

def write_node(state: NewsletterState):
    newsletter = text([SystemMessage(content=WRITER), HumanMessage(content=f"Goal: {state['goal']}\nArticles:\n{json.dumps(state['selected_articles'], ensure_ascii=False)}")])
    return {"newsletter": newsletter, "revision_count": state.get("revision_count", 0), "logs": state.get("logs", []) + ["Newsletter generated"]}

def critique_node(state: NewsletterState):
    critique = text([SystemMessage(content=CRITIC), HumanMessage(content=state["newsletter"])])
    return {"critique": critique, "logs": state.get("logs", []) + ["Self-critique completed"]}

def revise_node(state: NewsletterState):
    revised = text([SystemMessage(content=REVISER), HumanMessage(content=f"NEWSLETTER:\n{state['newsletter']}\n\nCRITIQUE:\n{state['critique']}")])
    return {"newsletter": revised, "revision_count": state.get("revision_count", 0) + 1, "logs": state.get("logs", []) + ["Newsletter revised"]}

def hitl_node(state: NewsletterState):
    decision = interrupt({"message": "Review the generated newsletter. Approve it or provide replacement HTML.", "newsletter": state["newsletter"]})
    if isinstance(decision, dict) and decision.get("approved"):
        return {"approved": True, "newsletter": decision.get("newsletter", state["newsletter"])}
    if isinstance(decision, str):
        return {"approved": True, "newsletter": decision}
    return {"approved": bool(decision)}

def output_node(state: NewsletterState):
    out = Path("output"); out.mkdir(exist_ok=True)
    path = out / "newsletter.html"
    path.write_text(state["newsletter"], encoding="utf-8")
    return {"output_path": str(path), "logs": state.get("logs", []) + [f"Newsletter saved to {path}"]}

def should_revise(state):
    return "revise" if state.get("revision_count", 0) < 1 else "hitl_or_output"

def hitl_or_output(state):
    return "hitl" if state.get("mode") == "hitl" else "output"

builder = StateGraph(NewsletterState)
for name, node in [("plan", plan_node), ("research", research_node), ("select", select_node), ("write", write_node), ("critique", critique_node), ("revise", revise_node), ("hitl", hitl_node), ("output", output_node)]:
    builder.add_node(name, node)
builder.add_edge(START, "plan"); builder.add_edge("plan", "research"); builder.add_edge("research", "select"); builder.add_edge("select", "write"); builder.add_edge("write", "critique")
builder.add_conditional_edges("critique", should_revise, {"revise": "revise", "hitl_or_output": "hitl_or_output"})
builder.add_edge("revise", "critique")
builder.add_conditional_edges("hitl_or_output", hitl_or_output, {"hitl": "hitl", "output": "output"})
builder.add_edge("hitl", "output"); builder.add_edge("output", END)

graph = builder.compile(checkpointer=InMemorySaver())

def run_newsletter_agent(goal: str, mode: str = "autonomous", thread_id: str = "newsletter-demo"):
    return graph.invoke({"goal": goal, "mode": mode, "logs": [], "revision_count": 0}, {"configurable": {"thread_id": thread_id}})

def resume_newsletter_agent(thread_id: str, response: Any):
    return graph.invoke(Command(resume=response), {"configurable": {"thread_id": thread_id}})
