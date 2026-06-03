import streamlit as st
import time
from pipeline import run_research_pipline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0a0f;
    color: #e8e6f0;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; }

/* Hero title */
.hero-title {
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.1;
    background: linear-gradient(135deg, #a78bfa 0%, #38bdf8 50%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}
.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #6b7280;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* Input area */
.stTextInput > div > div > input {
    background: #12121c !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 10px !important;
    color: #e8e6f0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1.05rem !important;
    padding: 0.85rem 1.1rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.18) !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 2.2rem !important;
    letter-spacing: 0.03em;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* Step cards */
.step-card {
    background: #12121c;
    border: 1px solid #1e1e30;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.step-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #7c3aed, #38bdf8);
}
.step-card.active::before {
    background: linear-gradient(90deg, #f59e0b, #f97316);
    animation: shimmer 1.2s infinite;
}
.step-card.done::before {
    background: linear-gradient(90deg, #10b981, #34d399);
}
@keyframes shimmer {
    0%   { opacity: 1; }
    50%  { opacity: 0.5; }
    100% { opacity: 1; }
}

.step-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 0.3rem;
}
.step-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #e8e6f0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.step-status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #374151;
    display: inline-block;
}
.step-status-dot.active { background: #f59e0b; animation: pulse 1s infinite; }
.step-status-dot.done   { background: #10b981; }
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.6; transform: scale(1.3); }
}

/* Output expander / text area */
.output-box {
    background: #0d0d18;
    border: 1px solid #1e1e30;
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.7;
    color: #c4bfdd;
    max-height: 320px;
    overflow-y: auto;
    margin-top: 0.8rem;
    white-space: pre-wrap;
    word-break: break-word;
}
.output-box::-webkit-scrollbar { width: 5px; }
.output-box::-webkit-scrollbar-track { background: #0d0d18; }
.output-box::-webkit-scrollbar-thumb { background: #2a2a40; border-radius: 3px; }

/* Divider */
hr { border-color: #1e1e30 !important; margin: 2rem 0 !important; }

/* Metric chips */
.chip {
    display: inline-block;
    background: #1a1a2e;
    border: 1px solid #2a2a40;
    border-radius: 20px;
    padding: 0.25rem 0.8rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #9ca3af;
    margin-right: 0.5rem;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def status_icon(status: str) -> str:
    return {"idle": "○", "active": "◉", "done": "✓"}[status]


def render_step(label: str, title: str, status: str, content: str = ""):
    card_class = "step-card " + ("active" if status == "active" else "done" if status == "done" else "")
    dot_class  = "step-status-dot " + ("active" if status == "active" else "done" if status == "done" else "")
    icon = status_icon(status)
    st.markdown(f"""
    <div class="{card_class}">
        <div class="step-label">{label}</div>
        <div class="step-title">
            <span class="{dot_class}"></span>
            {icon} &nbsp;{title}
        </div>
        {"<div class='output-box'>" + content[:3000] + ("…" if len(content) > 3000 else "") + "</div>" if content else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state defaults ────────────────────────────────────────────────────
for key in ("running", "state", "step"):
    if key not in st.session_state:
        st.session_state[key] = False if key == "running" else {} if key == "state" else 0


# ── Layout ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Multi-Agent Research</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Search → Scrape → Write → Critique</div>', unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 1])
with col_input:
    topic = st.text_input("", placeholder="Enter a research topic…", label_visibility="collapsed", key="topic_input")
with col_btn:
    run_clicked = st.button("Run →", use_container_width=True)

st.markdown("---")

# ── Pipeline execution with live step updates ─────────────────────────────────
STEPS = [
    ("STEP 01", "Search Agent — finding information"),
    ("STEP 02", "Reader Agent — scraping top resources"),
    ("STEP 03", "Writer — drafting the report"),
    ("STEP 04", "Critic — reviewing the report"),
]

if run_clicked and topic.strip():
    st.session_state.running = True
    st.session_state.state   = {}
    st.session_state.step    = 0

    placeholders = [st.empty() for _ in STEPS]

    # Show all steps as idle first
    for i, (lbl, ttl) in enumerate(STEPS):
        with placeholders[i]:
            render_step(lbl, ttl, "idle")

    # ── Step 1: Search ────────────────────────────────────────────────────────
    with placeholders[0]:
        render_step(*STEPS[0], "active")

    from agent import build_search_agent
    search_agent  = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    st.session_state.state["search_result"] = search_result["messages"][-1].content

    with placeholders[0]:
        render_step(*STEPS[0], "done", st.session_state.state["search_result"])

    # ── Step 2: Reader ────────────────────────────────────────────────────────
    with placeholders[1]:
        render_step(*STEPS[1], "active")

    from agent import build_reader_agent
    reader_agent  = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}',"
            f"pick the most relevant URL scrape it for deeper content.\n\n"
            f"Search Results:\n{st.session_state.state['search_result'][:800]}"
        )]
    })
    st.session_state.state["scraped_content"] = reader_result["messages"][-1].content

    with placeholders[1]:
        render_step(*STEPS[1], "done", st.session_state.state["scraped_content"])

    # ── Step 3: Writer ────────────────────────────────────────────────────────
    with placeholders[2]:
        render_step(*STEPS[2], "active")

    from agent import writer_chain
    research_combined = (
        f"SEARCH RESULTS:\n{st.session_state.state['search_result']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{st.session_state.state['scraped_content']}"
    )
    st.session_state.state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })

    with placeholders[2]:
        render_step(*STEPS[2], "done", st.session_state.state["report"])

    # ── Step 4: Critic ────────────────────────────────────────────────────────
    with placeholders[3]:
        render_step(*STEPS[3], "active")

    from agent import critic_chain
    st.session_state.state["feedback"] = critic_chain.invoke({
        "report": st.session_state.state["report"]
    })

    with placeholders[3]:
        render_step(*STEPS[3], "done", st.session_state.state["feedback"])

    st.session_state.running = False

    # ── Final report panel ────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📄 Final Report")
    st.markdown(
        f'<div class="output-box" style="max-height:600px;font-size:0.82rem;">'
        f'{st.session_state.state["report"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 🧠 Critic Feedback")
    st.markdown(
        f'<div class="output-box" style="border-color:#2a1f40;max-height:400px;">'
        f'{st.session_state.state["feedback"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div style="margin-top:1.5rem">'
        f'<span class="chip">Topic: {topic}</span>'
        f'<span class="chip">4 agents completed</span>'
        f'</div>',
        unsafe_allow_html=True
    )

elif run_clicked and not topic.strip():
    st.warning("Please enter a research topic first.")

# ── Idle state: show skeleton steps ──────────────────────────────────────────
elif not st.session_state.running and not st.session_state.state:
    for lbl, ttl in STEPS:
        render_step(lbl, ttl, "idle")
