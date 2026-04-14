import math
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# -----------------------------
# 1) UI/스타일 함수
# -----------------------------
def inject_glassmorphism_css() -> None:
    """Apple 스타일의 글래스모피즘 느낌을 위한 CSS를 주입한다."""
    st.markdown(
        """
        <style>
            html, body, [class*="css"] {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
            }
            .stApp {
                background: radial-gradient(circle at 20% 20%, #eef4ff 0%, #e9f0ff 30%, #f4f7ff 60%, #f9fbff 100%);
            }
            .glass-card {
                background: rgba(255, 255, 255, 0.50);
                border: 1px solid rgba(255, 255, 255, 0.65);
                border-radius: 18px;
                padding: 1rem 1.2rem;
                box-shadow: 0 10px 30px rgba(50, 80, 130, 0.12);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                margin-bottom: 0.8rem;
            }
            .hero {
                background: linear-gradient(135deg, rgba(255,255,255,0.62), rgba(235,242,255,0.5));
                border-radius: 22px;
                padding: 1.3rem 1.4rem;
                border: 1px solid rgba(255,255,255,0.7);
                box-shadow: 0 10px 24px rgba(52, 88, 140, 0.14);
                margin-bottom: 1rem;
            }
            .small-note {
                font-size: 0.92rem;
                color: #334155;
                line-height: 1.5;
            }
            .result-box {
                background: rgba(226, 240, 255, 0.5);
                border-left: 5px solid #3b82f6;
                border-radius: 12px;
                padding: 0.9rem 1rem;
                margin-top: 0.5rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="glass-card">
            <h4 style="margin:0 0 0.5rem 0; color:#1e3a8a;">{title}</h4>
            <div class="small-note">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# 2) 수열 생성 및 재구성 함수
# -----------------------------
def generate_arithmetic(a1: float, d: float, n_terms: int) -> Tuple[np.ndarray, np.ndarray]:
    idx = np.arange(1, n_terms + 1)
    values = a1 + (idx - 1) * d
    return idx, values


def generate_geometric(g1: float, r: float, n_terms: int) -> Tuple[np.ndarray, np.ndarray]:
    idx = np.arange(1, n_terms + 1)
    values = g1 * (r ** (idx - 1))
    return idx, values


def reconstruct_arithmetic(
    mode: str,
    a1: float,
    d: float,
    n_terms: int,
    k: float,
    b1: float,
    db: float,
) -> Dict:
    n, a_vals = generate_arithmetic(a1, d, n_terms)
    b_vals = b1 + (n - 1) * db

    if mode == "원래 등차수열 (aₙ)":
        new_vals = a_vals
        new_a1, new_d = a1, d
        expr = f"a_n = {a1:.3g} + (n-1)·{d:.3g}"
        explain = "원래 수열이므로 당연히 등차수열이며 공차는 그대로 유지됩니다."
    elif mode == "스칼라배 (k·aₙ)":
        new_vals = k * a_vals
        new_a1, new_d = k * a1, k * d
        expr = f"a'_n = {k:.3g}({a1:.3g} + (n-1)·{d:.3g}) = {new_a1:.3g} + (n-1)·{new_d:.3g}"
        explain = "모든 항에 같은 수를 곱하면 항 사이의 차이도 같은 비율로 바뀌어 공차가 일정합니다."
    elif mode == "합 (aₙ + bₙ)":
        new_vals = a_vals + b_vals
        new_a1, new_d = a1 + b1, d + db
        expr = f"c_n = ({a1:.3g}+{b1:.3g}) + (n-1)·({d:.3g}+{db:.3g})"
        explain = "두 등차수열의 합은 첫째항의 합, 공차의 합으로 표현되어 다시 등차수열이 됩니다."
    else:  # 차 (aₙ - bₙ)
        new_vals = a_vals - b_vals
        new_a1, new_d = a1 - b1, d - db
        expr = f"c_n = ({a1:.3g}-{b1:.3g}) + (n-1)·({d:.3g}-{db:.3g})"
        explain = "두 등차수열의 차도 첫째항과 공차가 일정한 꼴이므로 등차수열입니다."

    return {
        "n": n,
        "values": new_vals,
        "a1": new_a1,
        "d": new_d,
        "expr": expr,
        "explain": explain,
    }


def reconstruct_geometric(
    mode: str,
    g1: float,
    r: float,
    n_terms: int,
    k: float,
    h1: float,
    s: float,
) -> Dict:
    n, g_vals = generate_geometric(g1, r, n_terms)
    h_vals = h1 * (s ** (n - 1))

    if mode == "원래 등비수열 (gₙ)":
        new_vals = g_vals
        new_g1, new_r = g1, r
        expr = f"g_n = {g1:.3g}·({r:.3g})^(n-1)"
        explain = "원래 수열이므로 공비가 일정한 등비수열입니다."
    elif mode == "스칼라배 (k·gₙ)":
        new_vals = k * g_vals
        new_g1, new_r = k * g1, r
        expr = f"g'_n = {k:.3g}·{g1:.3g}·({r:.3g})^(n-1)"
        explain = "첫째항만 바뀌고 공비는 유지되므로 여전히 등비수열입니다."
    elif mode == "곱 (gₙ·hₙ)":
        new_vals = g_vals * h_vals
        new_g1, new_r = g1 * h1, r * s
        expr = f"p_n = ({g1:.3g}·{h1:.3g})·({r:.3g}·{s:.3g})^(n-1)"
        explain = "두 등비수열의 곱은 공비가 곱으로 결합되어 다시 등비수열이 됩니다."
    else:  # 나눗셈
        if abs(h1) < 1e-12:
            raise ValueError("h₁=0이면 첫 항부터 나눗셈이 정의되지 않습니다. h₁을 0이 아닌 값으로 바꿔 주세요.")
        if abs(s) < 1e-12 and n_terms >= 2:
            raise ValueError("h_n의 공비 s=0이면 n≥2에서 h_n=0이 되어 나눗셈이 정의되지 않습니다.")
        if np.any(np.isclose(h_vals, 0)):
            raise ValueError("일부 항에서 h_n=0이 되어 g_n / h_n을 계산할 수 없습니다. 입력값을 조정해 주세요.")

        new_vals = g_vals / h_vals
        new_g1, new_r = g1 / h1, r / s
        expr = f"q_n = ({g1:.3g}/{h1:.3g})·({r:.3g}/{s:.3g})^(n-1)"
        explain = "나눗셈이 모든 항에서 정의되면, 공비가 r/s로 일정하여 다시 등비수열이 됩니다."

    return {
        "n": n,
        "values": new_vals,
        "g1": new_g1,
        "r": new_r,
        "expr": expr,
        "explain": explain,
    }


# -----------------------------
# 3) Plotly 그래프 함수(애니메이션 포함)
# -----------------------------
def create_animated_sequence_function_plot(
    n_vals: np.ndarray,
    seq_vals: np.ndarray,
    func_x: np.ndarray,
    func_y: np.ndarray,
    seq_name: str,
    func_name: str,
) -> go.Figure:
    """수열 점 + 대응 함수 곡선을 순차적으로 보여주는 애니메이션 그래프"""
    total_steps = len(func_x)
    point_steps = np.linspace(1, total_steps, len(n_vals), dtype=int)

    frames = []
    for i in range(1, total_steps + 1):
        visible_points = point_steps <= i
        frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=func_x[:i],
                        y=func_y[:i],
                        mode="lines",
                        line=dict(color="#2563eb", width=3),
                        name=func_name,
                    ),
                    go.Scatter(
                        x=n_vals[visible_points],
                        y=seq_vals[visible_points],
                        mode="markers+text",
                        text=[f"a{int(v)}" for v in n_vals[visible_points]],
                        textposition="top center",
                        marker=dict(color="#f97316", size=10, line=dict(color="white", width=1)),
                        name=seq_name,
                    ),
                ],
                name=f"frame_{i}",
            )
        )

    fig = go.Figure(
        data=[
            go.Scatter(x=[], y=[], mode="lines", line=dict(color="#2563eb", width=3), name=func_name),
            go.Scatter(x=[], y=[], mode="markers", marker=dict(color="#f97316", size=10), name=seq_name),
        ],
        frames=frames,
    )

    fig.update_layout(
        title="수열의 점과 대응 함수의 연결(애니메이션)",
        xaxis_title="항 번호 n (또는 확장된 x)",
        yaxis_title="값",
        template="plotly_white",
        hovermode="x unified",
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "x": 0.0,
                "y": 1.12,
                "buttons": [
                    {
                        "label": "▶ 그래프 그리기",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 45, "redraw": True}, "fromcurrent": True}],
                    },
                    {
                        "label": "↺ 애니메이션 다시 보기",
                        "method": "animate",
                        "args": [[f"frame_{i}" for i in range(1, total_steps + 1)], {"frame": {"duration": 45, "redraw": True}, "fromcurrent": False}],
                    },
                ],
            }
        ],
        margin=dict(l=30, r=20, t=70, b=40),
    )
    return fig


# -----------------------------
# 4) 유틸 함수
# -----------------------------
def format_terms(values: np.ndarray, max_show: int = 8) -> str:
    selected = values[:max_show]
    text = ", ".join([f"{v:.4g}" for v in selected])
    if len(values) > max_show:
        text += ", ..."
    return text


def show_summary_box(lines: List[str]) -> None:
    joined = "<br>".join(lines)
    st.markdown(f"<div class='result-box'>{joined}</div>", unsafe_allow_html=True)


def validate_inputs(n_terms: int, ratio: float | None = None, positive_ratio_only: bool = False) -> Tuple[bool, str]:
    if n_terms < 2:
        return False, "항의 개수는 최소 2 이상이어야 규칙 변화를 관찰하기 좋습니다. 2 이상으로 조정해 주세요."
    if positive_ratio_only and ratio is not None and ratio <= 0:
        return False, "연속 지수함수와 직접 연결하려면 공비를 양수(r>0)로 제한하는 것이 적절합니다."
    return True, ""


# -----------------------------
# 5) 메인 앱
# -----------------------------
def main() -> None:
    st.set_page_config(page_title="등차·등비수열 재구성 탐구", layout="wide")
    inject_glassmorphism_css()

    st.markdown(
        """
        <div class="hero">
            <h2 style="margin:0; color:#0f172a;">등차수열과 등비수열의 재구성: 함수와 연결하여 이해하기</h2>
            <p style="margin:0.5rem 0 0.2rem 0; color:#1f2937;">수열의 점과 함수의 그래프를 비교하며 규칙의 구조를 탐구하는 수업용 앱</p>
            <p class="small-note" style="margin-top:0.6rem;">
            이 앱에서는 (1) 등차수열-일차함수, 등비수열-지수함수의 연결을 비교하고,
            (2) 수열을 재구성(합/차/스칼라배, 곱/나눗셈/스칼라배)했을 때 규칙이 어떻게 유지되는지 시각적으로 확인합니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tabs = st.tabs(["1) 개념 연결", "2) 비교 탐구", "3) 재구성 실험", "4) 학습 정리"])

    # -------- 탭1: 개념 연결 (선행조직자) --------
    with tabs[0]:
        render_card(
            "선행조직자: 기존 개념과 새로운 연결 만들기",
            "등차수열은 항 번호가 1씩 증가할 때 값이 일정하게 변하므로 자연수에서 정의된 <b>일차적 규칙</b>으로 볼 수 있습니다. "
            "등비수열은 항 번호가 1씩 증가할 때 값이 일정한 비율로 변하므로 자연수에서 정의된 <b>지수적 규칙</b>으로 이해할 수 있습니다.",
        )
        c1, c2 = st.columns(2)
        with c1:
            st.latex(r"a_n = a_1 + (n-1)d \quad \Longleftrightarrow \quad y = a_1 + (x-1)d")
            render_card(
                "등차수열 ↔ 일차함수",
                "수열은 떨어진 점(정의역: 자연수), 함수는 연속 그래프(정의역: 실수)이지만, 변화 규칙은 같은 일차 구조를 가집니다.",
            )
        with c2:
            st.latex(r"g_n = g_1 r^{n-1} \quad \Longleftrightarrow \quad y = g_1 r^{x-1}")
            render_card(
                "등비수열 ↔ 지수함수",
                "수열의 점들은 연속 지수곡선 위의 특정 지점으로 해석할 수 있습니다. 이때 연속 연결을 위해 보통 r>0으로 제한합니다.",
            )

    # -------- 탭2: 비교 탐구 (점진적 분화 1단계) --------
    with tabs[1]:
        st.markdown("### 수열의 점과 함수의 연속 그래프를 먼저 비교해 봅시다.")
        col_a, col_g = st.columns(2)

        with col_a:
            st.markdown("#### [A] 등차수열 vs 일차함수")
            ex_a = st.selectbox("등차 예시 불러오기", ["직접 입력", "예시1: a1=2, d=3", "예시2: a1=10, d=-2", "예시3: a1=-4, d=1.5"], key="ex_a")
            a1, d, n_a = 2.0, 3.0, 10
            if ex_a == "예시2: a1=10, d=-2":
                a1, d, n_a = 10.0, -2.0, 10
            elif ex_a == "예시3: a1=-4, d=1.5":
                a1, d, n_a = -4.0, 1.5, 10

            a1 = st.number_input("첫째항 a₁", value=a1, step=1.0, key="a1_cmp")
            d = st.number_input("공차 d", value=d, step=0.5, key="d_cmp")
            n_a = st.slider("항의 개수 n", 5, 25, n_a, key="n_a_cmp")

            valid, msg = validate_inputs(n_a)
            if not valid:
                st.warning(msg)
            else:
                n_vals, a_vals = generate_arithmetic(a1, d, n_a)
                x_cont = np.linspace(1, n_a + 1, 180)
                y_cont = a1 + (x_cont - 1) * d
                st.latex(fr"a_n = {a1:.3g} + (n-1){d:+.3g}")
                st.latex(fr"y = {a1:.3g} + (x-1){d:+.3g}")
                fig = create_animated_sequence_function_plot(n_vals, a_vals, x_cont, y_cont, "등차수열 점", "일차함수")
                st.plotly_chart(fig, use_container_width=True)

        with col_g:
            st.markdown("#### [B] 등비수열 vs 지수함수")
            ex_g = st.selectbox("등비 예시 불러오기", ["직접 입력", "예시1: g1=3, r=2", "예시2: g1=81, r=1/3", "예시3: g1=5, r=1"], key="ex_g")
            g1, r, n_g = 3.0, 2.0, 9
            if ex_g == "예시2: g1=81, r=1/3":
                g1, r, n_g = 81.0, 1 / 3, 9
            elif ex_g == "예시3: g1=5, r=1":
                g1, r, n_g = 5.0, 1.0, 9

            g1 = st.number_input("첫째항 g₁", value=g1, step=1.0, key="g1_cmp")
            r = st.number_input("공비 r (기본: 양수)", value=float(r), step=0.1, key="r_cmp")
            n_g = st.slider("항의 개수 n ", 5, 20, n_g, key="n_g_cmp")
            allow_negative = st.checkbox("심화 모드: 음수 공비 허용", value=False)

            valid, msg = validate_inputs(n_g, ratio=r, positive_ratio_only=not allow_negative)
            if not valid:
                st.warning(msg)
            else:
                n_vals, g_vals = generate_geometric(g1, r, n_g)
                st.latex(fr"g_n = {g1:.3g}\cdot({r:.3g})^{{n-1}}")

                if r > 0:
                    x_cont = np.linspace(1, n_g + 1, 220)
                    y_cont = g1 * np.power(r, x_cont - 1)
                    st.latex(fr"y = {g1:.3g}\cdot({r:.3g})^{{x-1}}")
                    fig = create_animated_sequence_function_plot(n_vals, g_vals, x_cont, y_cont, "등비수열 점", "지수함수")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("음수 공비에서는 실수 전체에서 연속 지수함수로 직접 확장하기 어렵습니다. 이 경우 수열 점 패턴 중심으로 해석하세요.")
                    x_cont = np.linspace(1, n_g, n_g)
                    y_cont = np.array([math.nan] * len(x_cont))
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=n_vals, y=g_vals, mode="markers+lines", name="등비수열 점"))
                    fig.update_layout(template="plotly_white", xaxis_title="n", yaxis_title="g_n")
                    st.plotly_chart(fig, use_container_width=True)

    # -------- 탭3: 재구성 실험 (점진적 분화 2단계 + 능동적 의미형성) --------
    with tabs[2]:
        st.markdown("### 수열을 재구성하고, 다시 같은 유형의 함수로 해석되는지 확인해 봅시다.")
        left, right = st.columns(2)

        with left:
            st.markdown("#### [A] 등차수열 재구성")
            a1 = st.number_input("a₁", value=2.0, key="a1_rec")
            d = st.number_input("d", value=3.0, key="d_rec")
            n_terms_a = st.slider("n (등차)", 5, 30, 10, key="n_rec_a")
            b1 = st.number_input("b₁ (두 번째 등차수열)", value=1.0, key="b1_rec")
            db = st.number_input("d_b", value=1.0, key="db_rec")
            k_a = st.number_input("k (스칼라배)", value=2.0, key="k_a_rec")
            mode_a = st.selectbox("재구성 선택", ["원래 등차수열 (aₙ)", "스칼라배 (k·aₙ)", "합 (aₙ + bₙ)", "차 (aₙ - bₙ)"], key="mode_a")

            if st.button("등차 재구성 실행", key="run_a"):
                result = reconstruct_arithmetic(mode_a, a1, d, n_terms_a, k_a, b1, db)
                st.latex(result["expr"].replace("·", r"\cdot "))
                st.write("처음 몇 개 항:", format_terms(result["values"]))
                st.caption(result["explain"])

                x_cont = np.linspace(1, n_terms_a + 1, 220)
                y_cont = result["a1"] + (x_cont - 1) * result["d"]
                fig = create_animated_sequence_function_plot(result["n"], result["values"], x_cont, y_cont, "재구성된 수열 점", "대응 일차함수")
                st.plotly_chart(fig, use_container_width=True)

                show_summary_box([
                    "<b>현재 선택한 재구성 결과는 등차수열입니다.</b>",
                    "대응 함수는 <b>일차함수</b>입니다.",
                    "수열은 점으로, 함수는 연속 그래프로 나타나지만 규칙 구조는 연결됩니다.",
                ])

        with right:
            st.markdown("#### [B] 등비수열 재구성")
            g1 = st.number_input("g₁", value=3.0, key="g1_rec")
            r = st.number_input("r (권장: 양수)", value=2.0, key="r_rec")
            n_terms_g = st.slider("n (등비)", 5, 20, 9, key="n_rec_g")
            h1 = st.number_input("h₁ (두 번째 등비수열)", value=1.0, key="h1_rec")
            s = st.number_input("s", value=0.5, key="s_rec")
            k_g = st.number_input("k (스칼라배)", value=2.0, key="k_g_rec")
            mode_g = st.selectbox("재구성 선택 ", ["원래 등비수열 (gₙ)", "스칼라배 (k·gₙ)", "곱 (gₙ·hₙ)", "나눗셈 (gₙ / hₙ)"], key="mode_g")
            allow_neg_rec = st.checkbox("심화 모드(재구성): 음수 공비 허용", value=False)

            if st.button("등비 재구성 실행", key="run_g"):
                if (not allow_neg_rec) and (r <= 0 or s <= 0):
                    st.warning("연속 지수함수와 연결해 해석하려면 r, s를 양수로 두는 것이 좋습니다. (심화 모드에서 음수 허용 가능)")
                else:
                    try:
                        result = reconstruct_geometric(mode_g, g1, r, n_terms_g, k_g, h1, s)
                        st.latex(result["expr"].replace("·", r"\cdot "))
                        st.write("처음 몇 개 항:", format_terms(result["values"]))
                        st.caption(result["explain"])

                        if result["r"] > 0:
                            x_cont = np.linspace(1, n_terms_g + 1, 250)
                            y_cont = result["g1"] * np.power(result["r"], x_cont - 1)
                            fig = create_animated_sequence_function_plot(result["n"], result["values"], x_cont, y_cont, "재구성된 수열 점", "대응 지수함수")
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            fig = go.Figure()
                            fig.add_trace(go.Scatter(x=result["n"], y=result["values"], mode="markers+lines", name="재구성된 수열"))
                            fig.update_layout(template="plotly_white", xaxis_title="n", yaxis_title="값")
                            st.plotly_chart(fig, use_container_width=True)
                            st.info("재구성 결과의 공비가 음수/0이면 연속 지수함수와 직접 대응시키기 어렵습니다. 점 패턴 해석 중심으로 살펴보세요.")

                        show_summary_box([
                            "<b>현재 선택한 재구성 결과는 등비수열입니다.</b>",
                            "대응 함수는 <b>지수함수</b>입니다(연속 연결은 보통 공비 양수에서 해석).",
                            "재구성해도 규칙 유형이 유지되는지 식과 그래프로 함께 확인하세요.",
                        ])
                    except ValueError as e:
                        st.error(f"입력 검토 안내: {e}")

    # -------- 탭4: 학습 정리 (통합적 조정) --------
    with tabs[3]:
        st.markdown("### 무엇을 알게 되었는가?")
        render_card(
            "통합적 조정: 차이와 연결을 함께 보기",
            "수열은 떨어진 점, 함수는 연속 그래프라는 표현 방식의 차이가 있습니다. "
            "하지만 등차수열-일차함수, 등비수열-지수함수는 같은 규칙 구조를 공유할 수 있습니다. "
            "재구성(합·차·스칼라배 / 곱·나눗셈·스칼라배) 후에도 유형이 유지되는지 스스로 설명해 보세요.",
        )

        reflection = st.text_area(
            "학습 정리 작성: ‘오늘 나는 ______를 비교하여 ______를 알게 되었다.’",
            height=120,
            placeholder="예) 등차수열의 점과 일차함수 그래프를 비교하여, 수열이 함수 위의 특정 x값에서의 점이라는 것을 알게 되었다.",
        )
        if reflection:
            st.success("좋습니다! 기존 개념(함수)과 새 관찰(재구성 결과)을 연결하여 설명한 점이 유의미 학습의 핵심입니다.")

        st.markdown("#### 수업 마무리 질문")
        st.markdown(
            """
            - 등차수열의 합/차/스칼라배가 다시 등차수열이 되는 이유를 **공차 관점**에서 설명해 보세요.
            - 등비수열의 곱/나눗셈/스칼라배가 다시 등비수열이 되는 이유를 **공비 관점**에서 설명해 보세요.
            - 수열의 점과 함수의 연속 그래프는 무엇이 다르고, 어떤 점에서 규칙이 같다고 볼 수 있나요?
            - 공비가 1, 0, 음수일 때 그래프 해석은 어떻게 달라지나요?
            - 오늘 탐구에서 가장 설득력 있었던 그래프 장면은 무엇이며, 왜 그렇게 생각했나요?
            """
        )

        st.markdown("---")
        st.markdown(
            """
            <div class="glass-card">
                <h4 style="margin-top:0; color:#1e3a8a;">교사용 활용 포인트</h4>
                <ul>
                    <li>"이 점들이 모두 같은 직선/곡선 위에 있다는 사실이 무엇을 의미하나요?"</li>
                    <li>"재구성 전후에 변한 것과 변하지 않은 것을 구분해 설명해 볼까요?"</li>
                    <li>"식, 표, 그래프 중 어떤 표현이 규칙 이해에 가장 도움이 되었나요?"</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption("실행 예시: streamlit run streamlit_app.py")


if __name__ == "__main__":
    main()

# 실행 명령어:
# streamlit run streamlit_app.py
