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
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
```

Add `OPENAI_API_KEY` and `TAVILY_API_KEY` to `.env`.

## Run locally

```bash
streamlit run app.py
```

## Demo goal

> Create a weekly newsletter on latest AI agent news and send it to our subscribers.

Choose **Fully Autonomous** for an end-to-end run or **Human-in-the-Loop** to pause for review before the simulated send.

## Deploy publicly with Streamlit Community Cloud

The app is ready to deploy from this GitHub repository. Streamlit Community Cloud can deploy a public GitHub repository directly and provides a `streamlit.app` URL.

1. Open [Streamlit Community Cloud](https://share.streamlit.io/).
2. Sign in with GitHub and authorize access to your public repositories.
3. Click **Create app** → **Yup, I have an app**.
4. Select repository `vipulbhat/newsletter-agent`.
5. Branch: `main`.
6. Main file: `app.py`.
7. Open **Advanced settings** → **Secrets** and add:

```toml
OPENAI_API_KEY = "your-openai-key"
TAVILY_API_KEY = "your-tavily-key"
OPENAI_MODEL = "gpt-5.6-luna"
```

8. Click **Deploy**.

Do not commit `.env` or `secrets.toml`. API keys belong in the hosting platform's secrets manager.

## Architecture

LangGraph orchestrates the explicit agentic stages and its checkpointer enables the HITL pause/resume flow.
