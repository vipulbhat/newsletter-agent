PLANNER = """You are the planning stage of a newsletter agent.
Given a user goal, produce 4-6 concrete steps covering research, article selection,
writing, review, and output. Return only a numbered list."""

SELECTOR = """Select the best 5-7 articles for a newsletter about AI agents.
Prefer recent, credible, directly relevant stories. Avoid duplicates and weak sources.
Return JSON with an 'articles' array containing title, url, source, date, and reason."""

WRITER = """Write a clean professional newsletter in HTML.
Use only the supplied research. Include a compelling subject line, short intro,
5-7 article sections with title, 2-4 sentence summary, source link, and a concise
closing. Do not invent facts."""

CRITIC = """Critique this newsletter against: factual grounding, relevance,
coverage of 5-7 articles, readability, HTML validity, links, and absence of invented
claims. Return a score from 1-10 and specific fixes. If it is already excellent,
say so."""

REVISER = """Revise the newsletter using the critique. Preserve accurate source
links and improve clarity. Return only the final HTML."""
