# Autonomous Newsletter Agent

A mini autonomous AI agent built for the AI Developer Assignment.

## Features

- Plain-English newsletter goal
- LangGraph workflow: plan → research → select → write → critique → revise → output
- Tavily web research
- LLM summarization and newsletter generation
- Self-critique and revision pass
- Single `run_newsletter_agent(goal, mode)` entry point
- Fully Autonomous / Human-in-the-Loop modes
- Streamlit frontend
- Simulated sending by saving `output/newsletter.html`

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
```

Add `OPENAI_API_KEY` and `TAVILY_API_KEY` to `.env`.

## Run

```bash
streamlit run app.py
```

## Demo goal

> Create a weekly newsletter on latest AI agent news and send it to our subscribers.

Choose **Fully Autonomous** for an end-to-end run or **Human-in-the-Loop** to pause for review before the simulated send.

## Architecture

LangGraph orchestrates the explicit agentic stages and its checkpointer enables the HITL pause/resume flow.
