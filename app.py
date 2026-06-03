import streamlit as st
import time

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #07070e;
    color: #e2dff5;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; padding-bottom: 4rem; max-width: 1200px; }

/* ── Hero ─────────────────────────────────────────────── */
.hero-wrap {
    padding: 3rem 0 2rem;
    border-bottom: 1px solid #1a1a2e;
    margin-bottom: 2rem;
}
.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #5b5b7e;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-size: clamp(2.6rem, 5vw, 4.2rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
    color: #e2dff5;
    margin-bottom: 0.5rem;
}
.hero-title span {
    background: linear-gradient(120deg, #818cf8, #38bdf8 45%, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-desc {
    font-size: 1rem;
    color: #6b6b90;
    max-width: 540px;
    line-height: 1.6;
}

/* ── Input row ────────────────────────────────────────── */
.stTextInput > div > div > input {
    background: #0f0f1a !important;
    border: 1.5px solid #252540 !important;
    border-radius: 12px !important;
    color: #e2dff5 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.9rem 1.2rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.9rem 2rem !important;
    letter-spacing: 0.04em;
    width: 100%;
}
.stButton > button:hover { filter: brightness(1.1) !important; }

/* ── Pipeline flow bar ────────────────────────────────── */
.pipeline-flow {
    display: flex;
    align-items: center;
    gap: 0;
    margin: 2rem 0 1.5rem;
    padding: 1.4rem 1.6rem;
    background: #0f0f1a;
    border: 1px solid #1a1a2e;
    border-radius: 16px;
    overflow-x: auto;
}
.pf-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    flex: 1;
    min-width: 110px;
}
.pf-icon {
    width: 52px; height: 52px;
    border-radius: 14px;
    border: 1.5px solid #252540;
    background: #13131f;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    transition: all 0.3s;
    position: relative;
}
.pf-icon.active {
    border-color: #f59e0b;
    background: #1c1608;
    box-shadow: 0 0 20px rgba(245,158,11,0.25);
    animation: icon-pulse 1.5s infinite;
}
.pf-icon.done {
    border-color: #10b981;
    background: #061710;
}
@keyframes icon-pulse {
    0%,100% { box-shadow: 0 0 20px rgba(245,158,11,0.2); }
    50%      { box-shadow: 0 0 30px rgba(245,158,11,0.5); }
}
.pf-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4b4b6e;
    text-align: center;
}
.pf-label.active { color: #f59e0b; }
.pf-label.done   { color: #10b981; }
.pf-connector {
    height: 1.5px;
    flex: 0.3;
    background: #1e1e30;
    margin-bottom: 28px;
    min-width: 20px;
}
.pf-connector.done { background: linear-gradient(90deg, #10b981, #059669); }
.pf-connector.active { background: linear-gradient(90deg, #10b981, #f59e0b); }

/* ── Progress bar ─────────────────────────────────────── */
.prog-wrap {
    background: #0f0f1a;
    border: 1px solid #1a1a2e;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.prog-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #5b5b7e;
    letter-spacing: 0.1em;
    white-space: nowrap;
    text-transform: uppercase;
}
.prog-bar-track {
    flex: 1;
    height: 6px;
    background: #1a1a2e;
    border-radius: 3px;
    overflow: hidden;
}
.prog-bar-fill {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, #6366f1, #38bdf8);
    transition: width 0.6s ease;
}
.prog-pct {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #818cf8;
    min-width: 32px;
    text-align: right;
}

/* ── Step cards ───────────────────────────────────────── */
.step-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    align-items: flex-start;
}
.step-timeline {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 1.4rem;
    flex-shrink: 0;
}
.step-dot {
    width: 12px; height: 12px;
    border-radius: 50%;
    background: #252540;
    border: 2px solid #1e1e30;
    z-index: 1;
}
.step-dot.active { background: #f59e0b; border-color: #f59e0b; animation: dot-pulse 1s infinite; }
.step-dot.done   { background: #10b981; border-color: #10b981; }
@keyframes dot-pulse {
    0%,100% { transform: scale(1); }
    50%      { transform: scale(1.4); }
}
.step-line {
    width: 2px;
    flex: 1;
    min-height: 30px;
    background: #1a1a2e;
    margin-top: 4px;
}
.step-line.done { background: #10b981; }
.step-card {
    flex: 1;
    background: #0f0f1a;
    border: 1px solid #1a1a2e;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.step-card.active {
    border-color: #f59e0b55;
    background: #110f07;
}
.step-card.done {
    border-color: #10b98133;
}
.step-card-accent {
    position: absolute;
    top: 0; left: 0;
    width: 3px;
    height: 100%;
    background: #252540;
    border-radius: 14px 0 0 14px;
}
.step-card-accent.active { background: linear-gradient(180deg, #f59e0b, #f97316); animation: shimmer-v 1.5s infinite; }
.step-card-accent.done   { background: linear-gradient(180deg, #10b981, #34d399); }
@keyframes shimmer-v {
    0%,100% { opacity: 1; }
    50%      { opacity: 0.5; }
}
.step-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.2rem;
}
.step-num {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #3d3d60;
}
.step-badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.step-badge.idle   { background: #1a1a2e; color: #3d3d60; border: 1px solid #252540; }
.step-badge.active { background: #1c1608; color: #f59e0b; border: 1px solid #f59e0b55; }
.step-badge.done   { background: #061710; color: #10b981; border: 1px solid #10b98133; }
.step-title {
    font-size: 1rem;
    font-weight: 600;
    color: #c4c0e0;
    margin-bottom: 0;
}
.step-card.active .step-title { color: #f5ecd4; }
.step-card.done .step-title   { color: #c4c0e0; }

/* ── Output box ───────────────────────────────────────── */
.output-wrap {
    margin-top: 0.8rem;
    border-top: 1px solid #1a1a2e;
    padding-top: 0.8rem;
}
.output-box {
    background: #090914;
    border: 1px solid #16162a;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    line-height: 1.8;
    color: #9e9bbf;
    max-height: 280px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}
.output-box::-webkit-scrollbar { width: 4px; }
.output-box::-webkit-scrollbar-track { background: transparent; }
.output-box::-webkit-scrollbar-thumb { background: #252540; border-radius: 2px; }

/* ── Stat cards ───────────────────────────────────────── */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.8rem;
    margin: 1.5rem 0;
}
.stat-card {
    background: #0f0f1a;
    border: 1px solid #1a1a2e;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    text-align: center;
}
.stat-val {
    font-size: 1.7rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.stat-lbl {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4b4b6e;
}

/* ── Final report ─────────────────────────────────────── */
.section-heading {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin: 2rem 0 1rem;
}
.section-heading-icon {
    width: 34px; height: 34px;
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}
.section-heading-icon.report { background: #0e0e22; border: 1px solid #2a2a50; }
.section-heading-icon.critic { background: #0e1a10; border: 1px solid #1a3020; }
.section-heading-text {
    font-size: 1.1rem;
    font-weight: 700;
    color: #c4c0e0;
    letter-spacing: -0.01em;
}
.report-box {
    background: #0c0c18;
    border: 1px solid #1e1e35;
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    font-size: 0.88rem;
    line-height: 1.85;
    color: #b8b4d5;
    max-height: 520px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}
.report-box::-webkit-scrollbar { width: 4px; }
.report-box::-webkit-scrollbar-thumb { background: #252540; border-radius: 2px; }

.critic-box {
    background: #090f0a;
    border: 1px solid #1a2e1e;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    font-size: 0.84rem;
    line-height: 1.85;
    color: #9ab8a0;
    max-height: 380px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}
.critic-box::-webkit-scrollbar { width: 4px; }
.critic-box::-webkit-scrollbar-thumb { background: #1a2e1e; border-radius: 2px; }

/* ── Completion banner ────────────────────────────────── */
.done-banner {
    background: linear-gradient(135deg, #061710 0%, #0a0a1a 100%);
    border: 1px solid #10b98133;
    border-radius: 14px;
    padding: 1.2rem 1.8rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1.5rem 0;
}
.done-banner-icon { font-size: 1.8rem; }
.done-banner-text { flex: 1; }
.done-banner-title {
    font-size: 1rem;
    font-weight: 700;
    color: #34d399;
    margin-bottom: 0.2rem;
}
.done-banner-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: #2d6b50;
    letter-spacing: 0.08em;
}

/* ── Chips ────────────────────────────────────────────── */
.chip-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1.2rem; }
.chip {
    background: #0f0f1a;
    border: 1px solid #252540;
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #5b5b7e;
    letter-spacing: 0.06em;
}
.chip.purple { border-color: #3730a355; color: #818cf8; background: #0c0c20; }
.chip.teal   { border-color: #10b98133; color: #34d399;  background: #061710; }

hr { border-color: #1a1a2e !important; margin: 1.8rem 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
STEP_META = [
    ("01", "Search Agent", "🔍", "Querying web for reliable sources"),
    ("02", "Reader Agent", "📖", "Scraping & extracting deep content"),
    ("03", "Writer",       "✍️",  "Drafting the structured report"),
    ("04", "Critic",       "🧠", "Reviewing & scoring the report"),
]

def badge_html(status):
    labels = {"idle": "Waiting", "active": "Running…", "done": "Done"}
    return f'<span class="step-badge {status}">{labels[status]}</span>'

def render_pipeline_flow(current_step: int):
    """current_step: 0=none done, 1=step1 active, 2=step1 done+step2 active…"""
    nodes_html = ""
    for i, (num, name, icon, _) in enumerate(STEP_META):
        if current_step == i + 1:
            state = "active"
        elif current_step > i + 1:
            state = "done"
        else:
            state = ""
        icon_disp = "✓" if state == "done" else icon
        nodes_html += f'''
        <div class="pf-node">
            <div class="pf-icon {state}">{icon_disp}</div>
            <div class="pf-label {state}">{name}</div>
        </div>'''
        if i < len(STEP_META) - 1:
            conn_state = "done" if current_step > i + 1 else ("active" if current_step == i + 1 else "")
            nodes_html += f'<div class="pf-connector {conn_state}"></div>'

    st.markdown(f'<div class="pipeline-flow">{nodes_html}</div>', unsafe_allow_html=True)

def render_progress(current_step: int):
    pct = int((current_step / len(STEP_META)) * 100)
    label = "Idle" if current_step == 0 else (f"Step {current_step} of {len(STEP_META)}" if current_step <= len(STEP_META) else "Complete")
    st.markdown(f'''
    <div class="prog-wrap">
        <span class="prog-label">{label}</span>
        <div class="prog-bar-track">
            <div class="prog-bar-fill" style="width:{pct}%"></div>
        </div>
        <span class="prog-pct">{pct}%</span>
    </div>''', unsafe_allow_html=True)

def render_step_card(idx: int, status: str, content: str = ""):
    num, name, icon, desc = STEP_META[idx]
    card_cls = status if status in ("active", "done") else ""
    output_html = ""
    if content:
        snippet = content[:2800] + ("…" if len(content) > 2800 else "")
        output_html = f'<div class="output-wrap"><div class="output-box">{snippet}</div></div>'
    st.markdown(f'''
    <div class="step-row">
        <div class="step-timeline">
            <div class="step-dot {status}"></div>
            <div class="step-line {"done" if status=="done" else ""}"></div>
        </div>
        <div class="step-card {card_cls}">
            <div class="step-card-accent {card_cls}"></div>
            <div class="step-card-header">
                <span class="step-num">Step {num}</span>
                {badge_html(status if status in ("active","done") else "idle")}
            </div>
            <div class="step-title">{icon}&nbsp; {name} — <span style="font-weight:400;color:#5b5b7e;font-size:0.88rem">{desc}</span></div>
            {output_html}
        </div>
    </div>''', unsafe_allow_html=True)

def render_stats(state: dict, topic: str):
    r_words  = len(state.get("report", "").split())
    s_words  = len(state.get("search_result", "").split())
    sc_words = len(state.get("scraped_content", "").split())
    st.markdown(f'''
    <div class="stats-grid">
        <div class="stat-card"><div class="stat-val">4</div><div class="stat-lbl">Agents run</div></div>
        <div class="stat-card"><div class="stat-val">{s_words}</div><div class="stat-lbl">Search tokens</div></div>
        <div class="stat-card"><div class="stat-val">{sc_words}</div><div class="stat-lbl">Scraped tokens</div></div>
        <div class="stat-card"><div class="stat-val">{r_words}</div><div class="stat-lbl">Report words</div></div>
    </div>''', unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("running", False), ("state", {}), ("cur_step", 0), ("done", False)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown('''
<div class="hero-wrap">
    <div class="hero-eyebrow">AI-Powered Intelligence</div>
    <div class="hero-title">Multi-Agent <span>Research</span></div>
    <div class="hero-desc">Four specialised agents collaborate — searching, reading, writing, and critiquing — to produce a deep research report on any topic.</div>
</div>''', unsafe_allow_html=True)


# ── Input ─────────────────────────────────────────────────────────────────────
col_in, col_btn = st.columns([5, 1])
with col_in:
    topic = st.text_input("", placeholder="Enter a research topic — e.g. 'Quantum computing 2025 breakthroughs'",
                          label_visibility="collapsed", key="topic_input")
with col_btn:
    run_clicked = st.button("▶  Run", use_container_width=True)

st.markdown("---")


# ── Pipeline ──────────────────────────────────────────────────────────────────
if run_clicked and topic.strip():
    st.session_state.running  = True
    st.session_state.state    = {}
    st.session_state.cur_step = 0
    st.session_state.done     = False

    flow_ph  = st.empty()
    prog_ph  = st.empty()
    step_phs = [st.empty() for _ in STEP_META]

    def refresh_idle():
        with flow_ph:  render_pipeline_flow(st.session_state.cur_step)
        with prog_ph:  render_progress(st.session_state.cur_step)

    # initial render
    refresh_idle()
    for i in range(len(STEP_META)):
        with step_phs[i]: render_step_card(i, "idle")

    # ── Step 1 ────────────────────────────────────────────────────────────────
    st.session_state.cur_step = 1
    refresh_idle()
    with step_phs[0]: render_step_card(0, "active")

    from agent import build_search_agent
    search_agent  = build_search_agent()
    res = search_agent.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]})
    st.session_state.state["search_result"] = res["messages"][-1].content

    with step_phs[0]: render_step_card(0, "done", st.session_state.state["search_result"])

    # ── Step 2 ────────────────────────────────────────────────────────────────
    st.session_state.cur_step = 2
    refresh_idle()
    with step_phs[1]: render_step_card(1, "active")

    from agent import build_reader_agent
    reader_agent  = build_reader_agent()
    res2 = reader_agent.invoke({"messages": [("user",
        f"Based on the following search results about '{topic}', "
        f"pick the most relevant URL scrape it for deeper content.\n\n"
        f"Search Results:\n{st.session_state.state['search_result'][:800]}")]})
    st.session_state.state["scraped_content"] = res2["messages"][-1].content

    with step_phs[1]: render_step_card(1, "done", st.session_state.state["scraped_content"])

    # ── Step 3 ────────────────────────────────────────────────────────────────
    st.session_state.cur_step = 3
    refresh_idle()
    with step_phs[2]: render_step_card(2, "active")

    from agent import writer_chain
    combined = (f"SEARCH RESULTS:\n{st.session_state.state['search_result']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{st.session_state.state['scraped_content']}")
    st.session_state.state["report"] = writer_chain.invoke({"topic": topic, "research": combined})

    with step_phs[2]: render_step_card(2, "done", st.session_state.state["report"])

    # ── Step 4 ────────────────────────────────────────────────────────────────
    st.session_state.cur_step = 4
    refresh_idle()
    with step_phs[3]: render_step_card(3, "active")

    from agent import critic_chain
    st.session_state.state["feedback"] = critic_chain.invoke({"report": st.session_state.state["report"]})

    with step_phs[3]: render_step_card(3, "done", st.session_state.state["feedback"])

    # ── Finish ────────────────────────────────────────────────────────────────
    st.session_state.cur_step = 5
    refresh_idle()
    st.session_state.running  = False
    st.session_state.done     = True

    # completion banner
    st.markdown(f'''
    <div class="done-banner">
        <div class="done-banner-icon">✅</div>
        <div class="done-banner-text">
            <div class="done-banner-title">Research complete</div>
            <div class="done-banner-sub">All 4 agents finished · Topic: {topic}</div>
        </div>
    </div>''', unsafe_allow_html=True)

    # stat cards
    render_stats(st.session_state.state, topic)

    # final report
    st.markdown('''
    <div class="section-heading">
        <div class="section-heading-icon report">📄</div>
        <div class="section-heading-text">Final Report</div>
    </div>''', unsafe_allow_html=True)
    st.markdown(f'<div class="report-box">{st.session_state.state["report"]}</div>', unsafe_allow_html=True)

    # critic feedback
    st.markdown('''
    <div class="section-heading">
        <div class="section-heading-icon critic">🧠</div>
        <div class="section-heading-text">Critic Feedback</div>
    </div>''', unsafe_allow_html=True)
    st.markdown(f'<div class="critic-box">{st.session_state.state["feedback"]}</div>', unsafe_allow_html=True)

    # tag chips
    st.markdown(f'''
    <div class="chip-row">
        <span class="chip purple">Research complete</span>
        <span class="chip teal">4 agents</span>
        <span class="chip">{topic[:40]}</span>
    </div>''', unsafe_allow_html=True)

elif run_clicked and not topic.strip():
    st.warning("Please enter a research topic first.")

# ── Idle state ────────────────────────────────────────────────────────────────
elif not st.session_state.running and not st.session_state.done:
    render_pipeline_flow(0)
    render_progress(0)
    for i in range(len(STEP_META)):
        render_step_card(i, "idle")