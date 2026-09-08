import streamlit as st
from agent import run_newsletter_agent, resume_newsletter_agent

st.set_page_config(page_title="Newsletter Agent", page_icon="📰", layout="wide")
st.title("📰 Autonomous Newsletter Agent")
st.caption("Plan → Research → Select → Write → Critique → Revise → Output")

goal = st.text_area("Newsletter goal", "Create a weekly newsletter on latest AI agent news and send it to our subscribers.", height=100)
mode_label = st.radio("Agent mode", ["Fully Autonomous", "Human-in-the-Loop"], horizontal=True)
mode = "autonomous" if mode_label == "Fully Autonomous" else "hitl"
if "thread_id" not in st.session_state: st.session_state.thread_id = "newsletter-ui"

if st.button("Run Newsletter Agent", type="primary"):
    with st.spinner("Agent is working..."):
        st.session_state.result = run_newsletter_agent(goal, mode, st.session_state.thread_id)

result = st.session_state.get("result")
if result:
    st.subheader("Agent activity")
    for log in result.get("logs", []): st.write("✓", log)
    if result.get("__interrupt__"):
        st.warning("Human review required.")
        html = result["__interrupt__"][0].value["newsletter"]
        st.components.v1.html(html, height=600, scrolling=True)
        edited = st.text_area("Optional replacement HTML", html, height=300)
        if st.button("Approve & Simulate Send"):
            st.session_state.result = resume_newsletter_agent(st.session_state.thread_id, {"approved": True, "newsletter": edited})
            st.rerun()
    else:
        st.subheader("Final newsletter")
        st.components.v1.html(result.get("newsletter", ""), height=700, scrolling=True)
        if result.get("output_path"): st.success(f"Simulated send complete. Saved to: {result['output_path']}")
