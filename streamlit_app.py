import math
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# -----------------------------
# UI 스타일 / 공통 렌더 함수
# -----------------------------
def inject_glassmorphism_css() -> None:
    """Apple 스타일의 글래스모피즘 느낌 CSS 주입"""
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 15% 20%, rgba(173, 216, 255, 0.35), transparent 40%),
                radial-gradient(circle at 85% 10%, rgba(220, 235, 255, 0.50), transparent 35%),
                linear-gradient(160deg, #eef3fb 0%, #e7edf7 45%, #eff4fc 100%);
            color: #1f2a44;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans KR", sans-serif;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.50);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.35);
            border-radius: 18px;
            padding: 18px 20px;
            margin-bottom: 14px;
            box-shadow: 0 8px 24px rgba(17, 40, 85, 0.10);
        }
        .header-card {
            background: rgba(255, 255, 255, 0.56);
            border-radius: 24px;
            padding: 24px 28px;
            border: 1px solid rgba(255,255,255,0.4);
            box-shadow: 0 12px 28px rgba(16, 45, 90, 0.12);
            margin-bottom: 20px;
        }
        .small-muted {
            color: #4c5e7f;
            font-size: 0.95rem;
        }
        .result-box {
            background: rgba(227, 240, 255, 0.55);
            border: 1px solid rgba(148, 185, 235, 0.45);
            border-radius: 14px;
            padding: 14px 16px;
            margin: 10px 0;
            color: #17345f;
        }
        .teacher-box {
            background: rgba(240, 248, 255, 0.62);
            border-left: 4px solid #4f81d9;
            border-radius: 10px;
            padding: 12px 14px;
            margin-top: 8px;
        }
        .kpi {
            font-weight: 700;
            color: #1b3865;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <div class="header-card">
            <h1 style="margin-bottom:8px;">등차수열과 등비수열의 재구성: 함수와 연결하여 이해하기</h1>
            <h4 style="margin-top:0; color:#355a8a;">수열의 점과 함수의 그래프를 비교하며 규칙의 구조를 탐구하는 수업용 앱</h4>
            <p class="small-muted">
                이 앱은 2차시 수업에서 <b>비교 → 재구성 → 통합적 이해</b>의 흐름으로 학습하도록 설계되었습니다.
                학생은 매개변수를 바꾸고 그래프를 애니메이션으로 관찰하며,
                수열의 규칙이 함수의 형태와 어떻게 연결되는지 스스로 의미를 구성할 수 있습니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_explanation_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="glass-card">
            <h4 style="margin: 0 0 8px 0;">{title}</h4>
            <p style="margin:0; line-height:1.7;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result_box(lines: List[str]) -> None:
    html = "".join([f"<li>{line}</li>" for line in lines])
    st.markdown(
        f"""
        <div class="result-box">
            <div class="kpi">결과 요약</div>
            <ul style="margin-top:8px; margin-bottom:2px;">{html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# 수열 생성 / 재구성 함수
# -----------------------------
def generate_arithmetic_sequence(a1: float, d: float, n_terms: int) -> Tuple[np.ndarray, np.ndarray]:
    n = np.arange(1, n_terms + 1)
    a_n = a1 + (n - 1) * d
    return n, a_n


def generate_geometric_sequence(g1: float, r: float, n_terms: int) -> Tuple[np.ndarray, np.ndarray]:
    n = np.arange(1, n_terms + 1)
    g_n = g1 * np.power(r, n - 1)
    return n, g_n


def reconstruct_arithmetic(
    op: str,
    a1: float,
    d: float,
    n_terms: int,
    k: float,
    b1: float,
    db: float,
) -> Dict[str, object]:
    n, a_n = generate_arithmetic_sequence(a1, d, n_terms)
    n2, b_n = generate_arithmetic_sequence(b1, db, n_terms)

    if op == "원래 등차수열 (a_n)":
        values = a_n
        new_a1, new_d = a1, d
        expr = f"a_n = {a1:.4g} + (n-1)({d:.4g})"
        why = "원래 수열이므로 등차수열입니다."
    elif op == "스칼라배 (k·a_n)":
        values = k * a_n
        new_a1, new_d = k * a1, k * d
        expr = f"a'_n = {k:.4g}[{a1:.4g} + (n-1)({d:.4g})] = {new_a1:.4g} + (n-1)({new_d:.4g})"
        why = "모든 항에 같은 수를 곱하면 항 사이 차이도 같은 비율로 바뀌어 공차가 일정합니다."
    elif op == "두 등차수열의 합 (a_n + b_n)":
        values = a_n + b_n
        new_a1, new_d = a1 + b1, d + db
        expr = (
            f"c_n = [{a1:.4g} + (n-1)({d:.4g})] + [{b1:.4g} + (n-1)({db:.4g})]"
            f" = {new_a1:.4g} + (n-1)({new_d:.4g})"
        )
        why = "두 수열의 각 항을 더하면 첫째항과 공차가 각각 더해져 여전히 공차가 일정합니다."
    else:
        values = a_n - b_n
        new_a1, new_d = a1 - b1, d - db
        expr = (
            f"c_n = [{a1:.4g} + (n-1)({d:.4g})] - [{b1:.4g} + (n-1)({db:.4g})]"
            f" = {new_a1:.4g} + (n-1)({new_d:.4g})"
        )
        why = "두 수열의 각 항을 빼면 첫째항과 공차가 각각 차가 되어도 공차가 일정합니다."

    return {
        "n": n,
        "values": values,
        "new_a1": new_a1,
        "new_d": new_d,
        "expr": expr,
        "why": why,
        "table": pd.DataFrame({"n": n, "재구성 수열": values}),
    }


def reconstruct_geometric(
    op: str,
    g1: float,
    r: float,
    n_terms: int,
    k: float,
    h1: float,
    s: float,
) -> Dict[str, object]:
    n, g_n = generate_geometric_sequence(g1, r, n_terms)
    _, h_n = generate_geometric_sequence(h1, s, n_terms)

    if op == "원래 등비수열 (g_n)":
        values = g_n
        new_g1, new_r = g1, r
        expr = f"g_n = {g1:.4g}·({r:.4g})^(n-1)"
        why = "원래 수열이므로 등비수열입니다."
    elif op == "스칼라배 (k·g_n)":
        values = k * g_n
        new_g1, new_r = k * g1, r
        expr = f"g'_n = {k:.4g}·{g1:.4g}·({r:.4g})^(n-1) = {new_g1:.4g}·({new_r:.4g})^(n-1)"
        why = "모든 항에 같은 수를 곱해도 인접한 항의 비는 유지되어 공비가 일정합니다."
    elif op == "두 등비수열의 곱 (g_n · h_n)":
        values = g_n * h_n
        new_g1, new_r = g1 * h1, r * s
        expr = (
            f"p_n = {g1:.4g}({r:.4g})^(n-1) · {h1:.4g}({s:.4g})^(n-1)"
            f" = {new_g1:.4g}·({new_r:.4g})^(n-1)"
        )
        why = "곱하면 첫째항은 곱으로, 공비도 곱으로 결합되어 여전히 등비수열입니다."
    else:
        if h1 == 0:
            raise ValueError("h₁이 0이면 첫 항에서 0으로 나눌 수 없습니다. h₁ ≠ 0으로 바꿔 주세요.")
        if s == 0 and n_terms > 1:
            raise ValueError("공비 s=0이면 h₂부터 0이 되어 나눗셈이 정의되지 않습니다. s를 0이 아닌 값으로 설정해 주세요.")
        if np.any(np.isclose(h_n, 0.0)):
            raise ValueError("h_n 중 0이 포함되어 나눗셈이 정의되지 않습니다. h₁, s 값을 조정해 주세요.")
        values = g_n / h_n
        new_g1, new_r = g1 / h1, r / s
        expr = (
            f"q_n = [{g1:.4g}({r:.4g})^(n-1)] / [{h1:.4g}({s:.4g})^(n-1)]"
            f" = {new_g1:.4g}·({new_r:.4g})^(n-1)"
        )
        why = "나눗셈도 정의역 조건(h_n≠0)을 만족하면 첫째항과 공비가 비로 결합되어 등비수열입니다."

    return {
        "n": n,
        "values": values,
        "new_g1": new_g1,
        "new_r": new_r,
        "expr": expr,
        "why": why,
        "table": pd.DataFrame({"n": n, "재구성 수열": values}),
    }


# -----------------------------
# Plotly 그래프 함수
# -----------------------------
def build_animation_figure(
    n_points: np.ndarray,
    seq_values: np.ndarray,
    x_cont: np.ndarray,
    y_cont: np.ndarray,
    seq_name: str,
    func_name: str,
    y_title: str,
) -> go.Figure:
    """점 + 연속함수를 순차적으로 그리는 Plotly 애니메이션"""
    frames = []
    total = len(x_cont)
    for i in range(2, total + 1):
        x_partial = x_cont[:i]
        y_partial = y_cont[:i]
        visible_points = n_points[n_points <= x_partial[-1]]
        point_values = seq_values[: len(visible_points)]

        frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=x_partial,
                        y=y_partial,
                        mode="lines",
                        name=func_name,
                        line=dict(color="#2d6cdf", width=3),
                    ),
                    go.Scatter(
                        x=visible_points,
                        y=point_values,
                        mode="markers",
                        name=seq_name,
                        marker=dict(color="#113b88", size=10, symbol="circle"),
                    ),
                ],
                name=str(i),
            )
        )

    fig = go.Figure(
        data=[
            go.Scatter(x=[x_cont[0]], y=[y_cont[0]], mode="lines", name=func_name, line=dict(color="#2d6cdf", width=3)),
            go.Scatter(x=[n_points[0]], y=[seq_values[0]], mode="markers", name=seq_name, marker=dict(color="#113b88", size=10)),
        ],
        frames=frames,
    )

    fig.update_layout(
        template="plotly_white",
        height=460,
        margin=dict(l=30, r=20, t=20, b=30),
        xaxis_title="항 번호 또는 x",
        yaxis_title=y_title,
        legend=dict(orientation="h", y=1.05, x=0),
        updatemenus=[
            {
                "type": "buttons",
                "direction": "left",
                "x": 0,
                "y": 1.18,
                "buttons": [
                    {
                        "label": "▶ 그래프 그리기",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 45, "redraw": True},
                                "transition": {"duration": 10},
                                "fromcurrent": True,
                            },
                        ],
                    },
                    {
                        "label": "↺ 애니메이션 다시 보기",
                        "method": "animate",
                        "args": [
                            [f.name for f in frames],
                            {
                                "frame": {"duration": 45, "redraw": True},
                                "transition": {"duration": 10},
                                "fromcurrent": False,
                            },
                        ],
                    },
                ],
            }
        ],
    )
    return fig


# -----------------------------
# 유틸 / 입력 예시 로딩
# -----------------------------
def init_state() -> None:
    defaults = {
        "arith": {"a1": 3.0, "d": 2.0, "n": 12, "b1": 1.0, "db": -1.0, "k": 2.0},
        "geo": {"g1": 2.0, "r": 1.5, "n": 10, "h1": 1.0, "s": 0.5, "k": 3.0},
    }
    if "params" not in st.session_state:
        st.session_state["params"] = defaults


def load_arith_example(idx: int) -> None:
    examples = [
        {"a1": 3.0, "d": 2.0, "n": 12, "b1": 1.0, "db": -1.0, "k": 2.0},
        {"a1": -4.0, "d": 3.0, "n": 10, "b1": 5.0, "db": 2.0, "k": -1.5},
        {"a1": 10.0, "d": -1.0, "n": 15, "b1": -2.0, "db": 4.0, "k": 0.5},
    ]
    st.session_state["params"]["arith"] = examples[idx]


def load_geo_example(idx: int) -> None:
    examples = [
        {"g1": 2.0, "r": 1.4, "n": 10, "h1": 1.0, "s": 0.7, "k": 3.0},
        {"g1": 64.0, "r": 0.5, "n": 10, "h1": 2.0, "s": 0.5, "k": 0.25},
        {"g1": -3.0, "r": 2.0, "n": 8, "h1": -1.0, "s": 2.0, "k": -2.0},
    ]
    st.session_state["params"]["geo"] = examples[idx]


def validate_common_n(n_terms: int) -> bool:
    if n_terms < 3 or n_terms > 40:
        st.warning("항의 개수 n은 3 이상 40 이하로 설정해 주세요. 그래프 관찰에 적절한 범위입니다.")
        return False
    return True


# -----------------------------
# 탭 렌더링
# -----------------------------
def render_tab_concept() -> None:
    render_explanation_card(
        "선행조직자(Advance Organizer)",
        "등차수열은 항 번호가 1씩 증가할 때 값이 일정하게 변하므로 자연수에서 정의된 일차적 규칙으로 볼 수 있습니다. "
        "등비수열은 항 번호가 1씩 증가할 때 값이 일정한 비율로 변하므로 자연수에서 정의된 지수적 규칙으로 이해할 수 있습니다.",
    )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 등차수열 ↔ 일차함수")
        st.latex(r"a_n = a_1 + (n-1)d")
        st.latex(r"y = a_1 + (x-1)d")
        st.info("수열은 자연수 n에서의 점, 함수는 실수 x에서의 연속 그래프입니다. 규칙 구조는 동일합니다.")
    with c2:
        st.markdown("### 등비수열 ↔ 지수함수")
        st.latex(r"g_n = g_1r^{n-1}")
        st.latex(r"y = g_1r^{x-1}")
        st.info("점(수열)과 곡선(함수)의 표현은 다르지만, 성장/감소의 핵심 규칙은 연결됩니다.")

    render_explanation_card(
        "통합적 조정(Integrative Reconciliation)",
        "수열은 떨어진 점, 함수는 연속 그래프라는 차이를 인식하되, 두 대상이 같은 형태의 규칙을 공유할 수 있음을 비교하며 확인해 봅시다.",
    )


def render_tab_compare() -> None:
    st.markdown("### 점진적 분화 1단계: 수열의 점과 대응 함수 비교")
    params_a = st.session_state["params"]["arith"]
    params_g = st.session_state["params"]["geo"]

    left, right = st.columns(2)
    with left:
        st.markdown("#### 등차수열 설정")
        if st.button("등차 예시 1", use_container_width=True):
            load_arith_example(0)
        if st.button("등차 예시 2", use_container_width=True):
            load_arith_example(1)
        if st.button("등차 예시 3", use_container_width=True):
            load_arith_example(2)

        params_a = st.session_state["params"]["arith"]
        a1 = st.number_input("a₁", value=float(params_a["a1"]), key="cmp_a1")
        d = st.number_input("d", value=float(params_a["d"]), key="cmp_d")
        n_a = st.slider("항의 개수 n", 3, 40, int(params_a["n"]), key="cmp_n_a")

        if validate_common_n(n_a):
            n, vals = generate_arithmetic_sequence(a1, d, n_a)
            x_cont = np.linspace(1, n_a, 220)
            y_cont = a1 + (x_cont - 1) * d
            st.latex(rf"a_n = {a1:.4g} + (n-1)({d:.4g})")
            st.latex(rf"y = {a1:.4g} + (x-1)({d:.4g})")
            fig = build_animation_figure(n, vals, x_cont, y_cont, "등차수열 점", "일차함수", "값")
            st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("#### 등비수열 설정")
        if st.button("등비 예시 1", use_container_width=True):
            load_geo_example(0)
        if st.button("등비 예시 2", use_container_width=True):
            load_geo_example(1)
        if st.button("등비 예시 3", use_container_width=True):
            load_geo_example(2)

        params_g = st.session_state["params"]["geo"]
        g1 = st.number_input("g₁", value=float(params_g["g1"]), key="cmp_g1")
        r = st.number_input("r (기본 모드: 양수 권장)", value=float(params_g["r"]), key="cmp_r")
        n_g = st.slider("항의 개수 n ", 3, 40, int(params_g["n"]), key="cmp_n_g")

        if validate_common_n(n_g):
            if r <= 0:
                st.warning("연속 지수함수와 직접 연결하려면 공비 r은 양수로 제한하는 것이 적절합니다. 현재는 점(수열) 중심으로 해석하세요.")
            n, vals = generate_geometric_sequence(g1, r, n_g)
            st.latex(rf"g_n = {g1:.4g}({r:.4g})^{{n-1}}")
            if r > 0:
                x_cont = np.linspace(1, n_g, 260)
                y_cont = g1 * np.power(r, x_cont - 1)
                st.latex(rf"y = {g1:.4g}({r:.4g})^{{x-1}}")
                fig = build_animation_figure(n, vals, x_cont, y_cont, "등비수열 점", "지수함수", "값")
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=n, y=vals, mode="markers+lines", name="등비수열 점", marker=dict(size=10)))
                fig.update_layout(template="plotly_white", height=430, xaxis_title="항 번호 n", yaxis_title="g_n")
                st.plotly_chart(fig, use_container_width=True)


def render_tab_reconstruct() -> None:
    st.markdown("### 점진적 분화 2단계: 재구성 실험 (학생 조작 중심)")
    col_a, col_g = st.columns(2)

    with col_a:
        st.markdown("#### A. 등차수열 재구성")
        a1 = st.number_input("기본 a₁", value=3.0, key="rec_a1")
        d = st.number_input("기본 d", value=2.0, key="rec_d")
        n_terms = st.slider("기본 n", 3, 40, 12, key="rec_na")
        b1 = st.number_input("두 번째 b₁", value=1.0, key="rec_b1")
        db = st.number_input("두 번째 d_b", value=-1.0, key="rec_db")
        k = st.number_input("스칼라 k", value=2.0, key="rec_ka")
        op = st.selectbox(
            "재구성 선택",
            ["원래 등차수열 (a_n)", "스칼라배 (k·a_n)", "두 등차수열의 합 (a_n + b_n)", "두 등차수열의 차 (a_n - b_n)"],
            key="op_a",
        )

        if st.button("등차 재구성 실행", use_container_width=True):
            result = reconstruct_arithmetic(op, a1, d, n_terms, k, b1, db)
            n = result["n"]
            vals = result["values"]
            new_a1, new_d = result["new_a1"], result["new_d"]
            st.success("재구성 완료! 결과가 다시 등차수열인지 확인해 보세요.")
            st.latex(rf"{result['expr']}")
            st.dataframe(result["table"].head(10), use_container_width=True)
            x_cont = np.linspace(1, n_terms, 240)
            y_cont = new_a1 + (x_cont - 1) * new_d
            fig = build_animation_figure(n, vals, x_cont, y_cont, "재구성 점", "대응 일차함수", "값")
            st.plotly_chart(fig, use_container_width=True)
            render_result_box([
                "현재 선택한 재구성 결과는 <b>등차수열</b>입니다.",
                "대응 함수는 <b>일차함수</b>입니다.",
                result["why"],
            ])

    with col_g:
        st.markdown("#### B. 등비수열 재구성")
        g1 = st.number_input("기본 g₁", value=2.0, key="rec_g1")
        r = st.number_input("기본 r (양수 권장)", value=1.5, key="rec_r")
        n_terms = st.slider("기본 n ", 3, 40, 10, key="rec_ng")
        h1 = st.number_input("두 번째 h₁", value=1.0, key="rec_h1")
        s = st.number_input("두 번째 s", value=0.5, key="rec_s")
        k = st.number_input("스칼라 k ", value=3.0, key="rec_kg")
        op = st.selectbox(
            "재구성 선택 ",
            ["원래 등비수열 (g_n)", "스칼라배 (k·g_n)", "두 등비수열의 곱 (g_n · h_n)", "두 등비수열의 나눗셈 (g_n / h_n)"],
            key="op_g",
        )

        if st.button("등비 재구성 실행", use_container_width=True):
            try:
                result = reconstruct_geometric(op, g1, r, n_terms, k, h1, s)
                n = result["n"]
                vals = result["values"]
                new_g1, new_r = result["new_g1"], result["new_r"]
                st.success("재구성 완료! 비의 구조가 유지되는지 관찰해 보세요.")
                st.latex(rf"{result['expr']}")
                st.dataframe(result["table"].head(10), use_container_width=True)
                if new_r > 0:
                    x_cont = np.linspace(1, n_terms, 280)
                    y_cont = new_g1 * np.power(new_r, x_cont - 1)
                    fig = build_animation_figure(n, vals, x_cont, y_cont, "재구성 점", "대응 지수함수", "값")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("새 공비가 0 이하이면 연속 지수함수로 직접 확장하기 어렵습니다. 점(수열) 관찰 중심으로 해석하세요.")
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=n, y=vals, mode="markers+lines", name="재구성 점"))
                    fig.update_layout(template="plotly_white", height=430, xaxis_title="항 번호 n", yaxis_title="값")
                    st.plotly_chart(fig, use_container_width=True)

                extra = "공비가 1이면 상수수열, 0<공비<1이면 감소, 공비>1이면 증가 패턴을 보입니다."
                if np.isclose(new_r, 1.0):
                    extra = "공비가 1이므로 모든 항이 같은 상수수열입니다."
                render_result_box([
                    "현재 선택한 재구성 결과는 <b>등비수열</b>입니다.",
                    "대응 함수는 <b>지수함수</b>입니다(공비 양수 조건).",
                    result["why"],
                    extra,
                ])
            except ValueError as e:
                st.error(f"입력값을 다시 확인해 주세요: {e}")
                st.info("수학적 정의역 조건을 점검하는 과정도 중요한 학습입니다. h_n이 0이 되지 않는지 확인해 봅시다.")


def render_tab_summary() -> None:
    render_explanation_card(
        "학습 정리: 무엇을 알게 되었는가?",
        "수열은 점, 함수는 연속 그래프라는 표현의 차이가 있지만 규칙의 형태를 공유할 수 있습니다. "
        "등차수열은 일차적 변화, 등비수열은 지수적 변화를 나타냅니다. 재구성을 해도 같은 구조가 유지되는지 식과 그래프로 확인해 보세요.",
    )

    st.markdown("#### 학생 정리 문장")
    st.text_area(
        "아래 문장을 완성해 보세요.",
        value=(
            "나는 오늘 ________ 수열을 ________ 방식으로 재구성했을 때,\n"
            "새 수열의 일반항이 ________ 꼴이 되어 다시 ________ 함수와 연결된다는 것을 확인했다."
        ),
        height=130,
    )

    st.markdown("#### 수업 마무리 질문")
    st.markdown(
        """
        1. 수열의 점과 함수의 연속 그래프는 무엇이 다르고, 무엇이 같은가?
        2. 등차수열의 합/차가 왜 다시 등차수열인지 일반항으로 설명할 수 있는가?
        3. 등비수열의 곱/나눗셈이 언제 가능한지 정의역 조건까지 말할 수 있는가?
        4. 공비가 1, 0, 음수일 때 그래프 해석은 어떻게 달라지는가?
        5. 재구성 결과를 그래프로 확인하는 과정이 식 이해에 어떤 도움을 주었는가?
        """
    )

    st.markdown(
        """
        <div class="teacher-box">
            <b>교사용 활용 포인트: 수업에서 이렇게 질문해 보세요</b>
            <ul>
                <li>"점으로 본 규칙과 곡선으로 본 규칙이 정확히 어디서 만나는가?"</li>
                <li>"재구성 전후에 바뀌는 것은 무엇이고, 보존되는 구조는 무엇인가?"</li>
                <li>"정의역 조건을 어기면 어떤 수학적 문제가 생기는가?"</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# 메인 앱
# -----------------------------
def main() -> None:
    st.set_page_config(page_title="등차·등비수열 재구성 수업 앱", layout="wide")
    inject_glassmorphism_css()
    init_state()
    render_header()

    tabs = st.tabs(["탭 1. 개념 연결", "탭 2. 비교 탐구", "탭 3. 재구성 실험", "탭 4. 학습 정리"])

    with tabs[0]:
        render_tab_concept()
    with tabs[1]:
        render_tab_compare()
    with tabs[2]:
        render_tab_reconstruct()
    with tabs[3]:
        render_tab_summary()

    st.caption("Ausubel의 유의미 학습 원리(선행조직자-점진적 분화-통합적 조정-능동적 의미 형성)를 반영한 2차시 수업 앱")


if __name__ == "__main__":
    main()

# 실행 방법:
# streamlit run streamlit_app.py
