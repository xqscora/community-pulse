"""
Community Pulse — Streamlit UI for Kaggle Gemma 4 hackathon demo.
Run: streamlit run app.py  (Ollama with Gemma model optional)
"""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from gemma_bridge import GemmaBridge, bridge_from_env
from simulation import CommunitySim, PolicyContext, load_scenario, list_scenarios

ROOT = Path(__file__).resolve().parent
SCENARIOS = ROOT / "scenarios"


def init_state() -> None:
    if "sim" not in st.session_state:
        st.session_state.sim = CommunitySim.fresh()
    if "bridge_fail" not in st.session_state:
        st.session_state.bridge_fail = None


def try_bridge() -> GemmaBridge | None:
    try:
        b = bridge_from_env()
        st.session_state.bridge_fail = None
        return b
    except Exception as exc:  # noqa: BLE001
        st.session_state.bridge_fail = str(exc)
        return None


def fig_drives_history(sim: CommunitySim) -> go.Figure | None:
    if not sim.history:
        return None
    names = {a.id: a.name for a in sim.agents}
    days = [h["day"] for h in sim.history]
    fig = go.Figure()
    for agent_row in sim.history[0]["agents"]:
        aid = agent_row["id"]
        ys = []
        for h in sim.history:
            for row in h["agents"]:
                if row["id"] == aid:
                    ys.append(sum(row["drives"].values()) / max(1, len(row["drives"])))
                    break
        fig.add_trace(
            go.Scatter(
                x=days[: len(ys)],
                y=ys,
                mode="lines+markers",
                name=names.get(aid, aid),
            )
        )
    fig.update_layout(
        title="Mean drive level over simulated days (per resident)",
        xaxis_title="Day",
        yaxis_title="Avg(drives)",
        height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    return fig


def fig_stress(sim: CommunitySim) -> go.Figure | None:
    if not sim.history:
        return None
    days = [h["day"] for h in sim.history]
    fig = go.Figure()
    for agent_row in sim.history[0]["agents"]:
        aid = agent_row["id"]
        name = next(a.name for a in sim.agents if a.id == aid)
        stress_vals = []
        for h in sim.history:
            for row in h["agents"]:
                if row["id"] == aid:
                    stress_vals.append(row["L4"].get("stress", 0))
                    break
        fig.add_trace(
            go.Scatter(x=days[: len(stress_vals)], y=stress_vals, name=name, mode="lines+markers")
        )
    fig.update_layout(
        title="L4 stress trace",
        xaxis_title="Day",
        yaxis_title="stress",
        height=360,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    return fig


def fig_community_metrics(sim: CommunitySim) -> go.Figure | None:
    rows = [h for h in sim.history if "metrics" in h]
    if not rows:
        return None
    days = [h["day"] for h in rows]
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=("Mean L4 stress", "Social cohesion (mean tie trust)", "Resilience index"),
    )
    fig.add_trace(
        go.Scatter(x=days, y=[h["metrics"]["mean_stress"] for h in rows], mode="lines+markers"),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=days, y=[h["metrics"]["social_cohesion_trust"] for h in rows], mode="lines+markers"
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(x=days, y=[h["metrics"]["resilience_index"] for h in rows], mode="lines+markers"),
        row=3,
        col=1,
    )
    fig.update_yaxes(range=[0, 1], row=1, col=1)
    fig.update_yaxes(range=[0, 1], row=2, col=1)
    fig.update_yaxes(range=[0, 1], row=3, col=1)
    fig.update_layout(
        title_text="Community aggregates (after each day)",
        height=520,
        showlegend=False,
    )
    fig.update_xaxes(title_text="Simulated day", row=3, col=1)
    return fig


def fig_drive_heatmap(sim: CommunitySim) -> go.Figure | None:
    if not sim.history:
        return None
    last = sim.history[-1]
    names = [row["name"] for row in last["agents"]]
    keys = list(last["agents"][0]["drives"].keys())
    z = [[row["drives"][k] for k in keys] for row in last["agents"]]
    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=keys,
            y=names,
            colorscale="Viridis",
            zmin=0,
            zmax=1,
        )
    )
    fig.update_layout(
        title=f"Drive profile — end of day {last['day']}",
        xaxis_title="drive",
        height=max(320, 28 * len(names)),
    )
    return fig


def fig_network(sim: CommunitySim) -> go.Figure:
    G = nx.Graph()
    for a in sim.agents:
        G.add_node(a.id, label=a.name.split()[0])
    for (u, v), m in sim.ties.items():
        G.add_edge(u, v, weight=m["trust"])
    if G.number_of_nodes() == 0:
        return go.Figure()
    pos = nx.spring_layout(G, seed=7, k=0.55)
    edge_x: list[float] = []
    edge_y: list[float] = []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.6, color="#888"),
        hoverinfo="none",
        mode="lines",
    )
    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]
    labels = [G.nodes[n]["label"] for n in G.nodes()]
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=labels,
        textposition="top center",
        hoverinfo="text",
        marker=dict(size=18, color="#4ECDC4", line=dict(width=1, color="#333")),
    )
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="Social ties (edges from seeded familiarity)",
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=400,
    )
    return fig


def main() -> None:
    st.set_page_config(page_title="Community Pulse", layout="wide")
    init_state()
    sim: CommunitySim = st.session_state.sim

    st.title("Community Pulse")
    st.caption(
        "Policy simulation with PAT Mini-Cerome drives + Gemma (Ollama). "
        "Hackathon build; personality engine from Zeng PAT / Cerome (CogArch)."
    )

    with st.sidebar:
        st.header("Policy")
        scenario_files = list_scenarios(SCENARIOS)
        labels = ["(custom)"] + [p.stem for p in scenario_files]
        choice = st.selectbox("Preset scenario", labels)
        custom_title = st.text_input("Policy title", value=sim.policy.title)
        custom_body = st.text_area("Policy description", value=sim.policy.description, height=120)
        c1, c2, c3 = st.columns(3)
        with c1:
            d_stress = st.number_input("Δ stress", value=0.0, step=0.05, format="%.2f")
        with c2:
            d_nov = st.number_input("Δ novelty", value=0.0, step=0.05, format="%.2f")
        with c3:
            d_ch = st.number_input("Δ challenge", value=0.0, step=0.05, format="%.2f")

        if st.button("Apply policy to simulation state"):
            if choice != "(custom)" and scenario_files:
                path = next(p for p in scenario_files if p.stem == choice)
                pol = load_scenario(path)
            else:
                pol = PolicyContext(
                    title=custom_title,
                    description=custom_body,
                    stress_delta=d_stress,
                    novelty_delta=d_nov,
                    challenge_delta=d_ch,
                )
            sim.apply_policy(pol)
            st.success("Policy applied (L4 deltas merged).")

        st.divider()
        model = st.text_input("Ollama model name", value="gemma3:4b")
        max_llm = st.slider("Max agents to call LLM per day", 0, 10, 6)
        pairs = st.slider("Dialogue pairs per day", 0, 5, 2)
        workers = st.slider("Parallel LLM workers", 1, 8, 4)

        graph_seed_in = st.text_input(
            "Graph seed (optional, integer; empty = random new graph)",
            value="",
            help="Same seed → same initial tie pattern. Day-level sampling uses Streamlit rerun state.",
        )
        if st.button("Reset simulation (new graph + agents)"):
            gs: int | None
            raw = graph_seed_in.strip()
            if raw == "":
                gs = None
            else:
                try:
                    gs = int(raw)
                except ValueError:
                    gs = None
                    st.warning("Invalid seed; using random graph.")
            st.session_state.sim = CommunitySim.fresh(random_seed=gs)
            st.rerun()

        run = st.button("Run one simulated day", type="primary")

        if st.session_state.sim.history:
            st.download_button(
                label="Download run history (JSON)",
                data=json.dumps(st.session_state.sim.history, indent=2, ensure_ascii=False),
                file_name="community_pulse_history.json",
                mime="application/json",
            )

    bridge = None
    if max_llm > 0 or pairs > 0:
        import os

        os.environ["OLLAMA_GEMMA_MODEL"] = model
        bridge = try_bridge()
        if st.session_state.bridge_fail:
            st.warning(f"Gemma bridge not available: {st.session_state.bridge_fail}")

    if run:
        sim.step_day(
            bridge,
            max_reason_llm=max_llm,
            dialogue_pairs=pairs,
            llm_workers=workers,
        )
        st.success(f"Finished day {sim.day - 1}.")

    if sim.history and "metrics" in sim.history[-1]:
        m = sim.history[-1]["metrics"]
        c0, c1, c2, c3 = st.columns(4)
        c0.metric("Mean L4 stress", f"{m['mean_stress']:.2f}")
        c1.metric("Social cohesion (trust)", f"{m['social_cohesion_trust']:.2f}")
        c2.metric("Resilience index", f"{m['resilience_index']:.2f}")
        c3.metric("Edges in graph", f"{int(m['n_edges'])}")

    col_a, col_b = st.columns((1.1, 1.0))
    with col_a:
        st.subheader("Dashboard")
        fm = fig_community_metrics(sim)
        if fm:
            st.plotly_chart(fm, use_container_width=True)
        fh = fig_drive_heatmap(sim)
        if fh:
            st.plotly_chart(fh, use_container_width=True)
        f1 = fig_stress(sim)
        if f1:
            st.plotly_chart(f1, use_container_width=True)
        f2 = fig_drives_history(sim)
        if f2:
            st.plotly_chart(f2, use_container_width=True)
        st.plotly_chart(fig_network(sim), use_container_width=True)

    with col_b:
        st.subheader("Residents")
        for a in sim.agents:
            with st.expander(f"{a.name} — {a.role}"):
                st.write(a.backstory)
                st.json({"drives": a.drives(), "L4": a.cerome.L4, "L1": a.cerome.L1})
                if a.last_reaction:
                    st.markdown("**Latest reaction**")
                    st.write(a.last_reaction)

        st.subheader("Day summary (Gemma)")
        if sim.last_summary:
            st.write(sim.last_summary)
        else:
            st.info("Run a day with LLM enabled to produce a summary.")

        st.subheader("Dialogue log")
        st.text_area(
            "dialogue",
            value="\n\n".join(sim.dialogue_log[-12:]) if sim.dialogue_log else "(empty)",
            height=320,
        )


if __name__ == "__main__":
    main()
