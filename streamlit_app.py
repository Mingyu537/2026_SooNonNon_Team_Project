import time
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
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
                학생은 매개변수를 바꾸고 그래프 전개 과정을 관찰하며,
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


def reconstruct_arithmetic(op: str, a1: float, d: float, n_terms: int, k: float, b1: float, db: float) -> Dict[str, object]:
    n, a_n = generate_arithmetic_sequence(a1, d, n_terms)
    _, b_n = generate_arithmetic_sequence(b1, db, n_terms)

    if op == "원래 등차수열 (a_n)":
        values = a_n
        new_a1, new_d = a1, d
        expr = f"a_n = {a1:.4g} + (n-1)({d:.4g})"
        why = "원래 수열이므로 등차수열입니다."
    elif op == "스칼라배 (k·a_n)":
        values = k * a_n
        new_a1, new_d = k * a1, k * d
        expr = f"a'_n = {k:.4g}[{a1:.4g} + (n-1)({d:.4g})] = {new_a1:.4g} + (n-1)({new_d:.4g})"
        why = "모든 항에 같은 수를 곱하면 공차도 같은 비율로 바뀌어 일정합니다."
    elif op == "두 등차수열의 합 (a_n + b_n)":
        values = a_n + b_n
        new_a1, new_d = a1 + b1, d + db
        expr = f"c_n = {new_a1:.4g} + (n-1)({new_d:.4g})"
        why = "합의 첫째항과 공차가 각각 더해져 공차가 일정합니다."
    else:
        values = a_n - b_n
        new_a1, new_d = a1 - b1, d - db
        expr = f"c_n = {new_a1:.4g} + (n-1)({new_d:.4g})"
        why = "차의 첫째항과 공차가 각각 차가 되어도 공차가 일정합니다."

    return {"n": n, "values": values, "new_a1": new_a1, "new_d": new_d, "expr": expr, "why": why}


def reconstruct_geometric(op: str, g1: float, r: float, n_terms: int, k: float, h1: float, s: float) -> Dict[str, object]:
    n, g_n = generate_geometric_sequence(g1, r, n_terms)
    _, h_n = generate_geometric_sequence(h1, s, n_terms)

    if op == "원래 등비수열 (g_n)":
        values = g_n
        new_g1, new_r = g1, r
        expr = f"g_n = {g1:.4g}({r:.4g})^(n-1)"
        why = "원래 수열이므로 등비수열입니다."
    elif op == "스칼라배 (k·g_n)":
        values = k * g_n
        new_g1, new_r = k * g1, r
        expr = f"g'_n = {new_g1:.4g}({new_r:.4g})^(n-1)"
        why = "스칼라배는 공비를 유지하므로 등비수열입니다."
    elif op == "두 등비수열의 곱 (g_n · h_n)":
        values = g_n * h_n
        new_g1, new_r = g1 * h1, r * s
        expr = f"p_n = {new_g1:.4g}({new_r:.4g})^(n-1)"
        why = "곱의 첫째항/공비가 각각 곱으로 결합되어 등비수열입니다."
    else:
        if h1 == 0:
            raise ValueError("h₁이 0이면 첫 항에서 나눗셈이 불가능합니다. h₁ ≠ 0으로 바꿔 주세요.")
        if s == 0 and n_terms > 1:
            raise ValueError("s=0이면 h₂부터 0이 되어 나눗셈이 정의되지 않습니다.")
        if np.any(np.isclose(h_n, 0.0)):
            raise ValueError("h_n 중 0이 있어 나눗셈이 정의되지 않습니다. h₁, s를 조정해 주세요.")
        values = g_n / h_n
        new_g1, new_r = g1 / h1, r / s
        expr = f"q_n = {new_g1:.4g}({new_r:.4g})^(n-1)"
        why = "정의역 조건(h_n≠0)을 만족하면 나눗셈 결과도 등비수열입니다."

    return {"n": n, "values": values, "new_g1": new_g1, "new_r": new_r, "expr": expr, "why": why}


# -----------------------------
# 애니메이션(Plotly 미사용)
# -----------------------------
def create_discrete_df(n: np.ndarray, y: np.ndarray, name: str) -> pd.DataFrame:
    return pd.DataFrame({"n": n, name: y})


def create_continuous_df(x: np.ndarray, y: np.ndarray, name: str) -> pd.DataFrame:
    return pd.DataFrame({"x": x, name: y})


def animate_sequence_and_function(
    n: np.ndarray,
    y_seq: np.ndarray,
    x_cont: np.ndarray,
    y_cont: np.ndarray,
    seq_name: str,
    func_name: str,
    run_animation: bool,
    speed_sec: float = 0.03,
) -> None:
    """st.line_chart + st.scatter_chart를 반복 업데이트하여 애니메이션 효과 제공"""
    line_placeholder = st.empty()
    point_placeholder = st.empty()

    if not run_animation:
        cont_df = create_continuous_df(x_cont, y_cont, func_name).set_index("x")
        seq_df = create_discrete_df(n, y_seq, seq_name).set_index("n")
        line_placeholder.line_chart(cont_df, height=320)
        point_placeholder.scatter_chart(seq_df, height=320)
        return

    steps = len(x_cont)
    for i in range(5, steps + 1, 5):
        x_part = x_cont[:i]
        y_part = y_cont[:i]
        visible = n <= x_part[-1]

        cont_df = create_continuous_df(x_part, y_part, func_name).set_index("x")
        seq_df = create_discrete_df(n[visible], y_seq[: np.sum(visible)], seq_name).set_index("n")

        line_placeholder.line_chart(cont_df, height=320)
        point_placeholder.scatter_chart(seq_df, height=320)
        time.sleep(speed_sec)


# -----------------------------
# 유틸 / 예시 입력
# -----------------------------
def init_state() -> None:
    if "params" not in st.session_state:
        st.session_state["params"] = {
            "arith": {"a1": 3.0, "d": 2.0, "n": 12, "b1": 1.0, "db": -1.0, "k": 2.0},
            "geo": {"g1": 2.0, "r": 1.5, "n": 10, "h1": 1.0, "s": 0.5, "k": 3.0},
        }


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


# -----------------------------
# 탭 렌더링
# -----------------------------
def render_tab_concept() -> None:
    render_explanation_card(
        "선행조직자(Advance Organizer)",
        "등차수열은 자연수에서 정의된 일차적 규칙, 등비수열은 자연수에서 정의된 지수적 규칙으로 이해할 수 있습니다. "
        "이미 배운 일차함수·지수함수와 연결하여 새로운 관계를 재구성해 봅시다.",
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 등차수열 ↔ 일차함수")
        st.latex(r"a_n = a_1 + (n-1)d")
        st.latex(r"y = a_1 + (x-1)d")
        st.info("수열은 점, 함수는 연속 그래프이지만 변화 규칙은 같은 구조를 가질 수 있습니다.")

    with c2:
        st.markdown("### 등비수열 ↔ 지수함수")
        st.latex(r"g_n = g_1r^{n-1}")
        st.latex(r"y = g_1r^{x-1}")
        st.info("항 번호가 1씩 증가할 때 일정한 비율 변화가 나타나는지 관찰해 봅시다.")


def render_tab_compare() -> None:
    st.markdown("### 점진적 분화 1단계: 수열의 점과 대응 함수 비교")
    left, right = st.columns(2)

    with left:
        st.markdown("#### 등차수열")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("등차 예시 1", use_container_width=True):
                load_arith_example(0)
        with c2:
            if st.button("등차 예시 2", use_container_width=True):
                load_arith_example(1)
        with c3:
            if st.button("등차 예시 3", use_container_width=True):
                load_arith_example(2)

        p = st.session_state["params"]["arith"]
        a1 = st.number_input("a₁", value=float(p["a1"]), key="cmp_a1")
        d = st.number_input("d", value=float(p["d"]), key="cmp_d")
        n_terms = st.slider("n", 3, 40, int(p["n"]), key="cmp_an")
        run = st.button("그래프 그리기 (등차)", use_container_width=True)

        n, a_n = generate_arithmetic_sequence(a1, d, n_terms)
        x = np.linspace(1, n_terms, 300)
        y = a1 + (x - 1) * d

        st.latex(rf"a_n = {a1:.4g} + (n-1)({d:.4g})")
        st.latex(rf"y = {a1:.4g} + (x-1)({d:.4g})")

        animate_sequence_and_function(n, a_n, x, y, "등차수열 점", "일차함수", run_animation=run)

    with right:
        st.markdown("#### 등비수열")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("등비 예시 1", use_container_width=True):
                load_geo_example(0)
        with c2:
            if st.button("등비 예시 2", use_container_width=True):
                load_geo_example(1)
        with c3:
            if st.button("등비 예시 3", use_container_width=True):
                load_geo_example(2)

        p = st.session_state["params"]["geo"]
        g1 = st.number_input("g₁", value=float(p["g1"]), key="cmp_g1")
        r = st.number_input("r (기본 모드: 양수 권장)", value=float(p["r"]), key="cmp_r")
        n_terms = st.slider("n ", 3, 40, int(p["n"]), key="cmp_gn")
        run = st.button("그래프 그리기 (등비)", use_container_width=True)

        n, g_n = generate_geometric_sequence(g1, r, n_terms)
        st.latex(rf"g_n = {g1:.4g}({r:.4g})^{{n-1}}")

        if r > 0:
            x = np.linspace(1, n_terms, 300)
            y = g1 * np.power(r, x - 1)
            st.latex(rf"y = {g1:.4g}({r:.4g})^{{x-1}}")
            animate_sequence_and_function(n, g_n, x, y, "등비수열 점", "지수함수", run_animation=run)
        else:
            st.warning("연속 지수함수와 직접 연결하려면 r>0 조건이 필요합니다. 현재는 수열 점만 해석합니다.")
            seq_df = create_discrete_df(n, g_n, "등비수열 점").set_index("n")
            st.scatter_chart(seq_df, height=320)


def render_tab_reconstruct() -> None:
    st.markdown("### 점진적 분화 2단계: 재구성 실험")
    left, right = st.columns(2)

    with left:
        st.markdown("#### A. 등차수열 재구성")
        a1 = st.number_input("기본 a₁", value=3.0, key="ra1")
        d = st.number_input("기본 d", value=2.0, key="rd")
        n_terms = st.slider("기본 n", 3, 40, 12, key="ran")
        b1 = st.number_input("두 번째 b₁", value=1.0, key="rb1")
        db = st.number_input("두 번째 d_b", value=-1.0, key="rdb")
        k = st.number_input("스칼라 k", value=2.0, key="rak")
        op = st.selectbox("연산 선택", ["원래 등차수열 (a_n)", "스칼라배 (k·a_n)", "두 등차수열의 합 (a_n + b_n)", "두 등차수열의 차 (a_n - b_n)"])
        run = st.button("등차 재구성 실행", use_container_width=True)

        if run:
            res = reconstruct_arithmetic(op, a1, d, n_terms, k, b1, db)
            n, y = res["n"], res["values"]
            st.latex(res["expr"])
            st.dataframe(pd.DataFrame({"n": n, "재구성 수열": y}).head(10), use_container_width=True)
            x = np.linspace(1, n_terms, 300)
            y_cont = res["new_a1"] + (x - 1) * res["new_d"]
            animate_sequence_and_function(n, y, x, y_cont, "재구성 점", "대응 일차함수", run_animation=True)
            render_result_box([
                "현재 선택한 재구성 결과는 <b>등차수열</b>입니다.",
                "대응 함수는 <b>일차함수</b>입니다.",
                res["why"],
            ])

    with right:
        st.markdown("#### B. 등비수열 재구성")
        g1 = st.number_input("기본 g₁", value=2.0, key="rg1")
        r = st.number_input("기본 r", value=1.5, key="rr")
        n_terms = st.slider("기본 n ", 3, 40, 10, key="rgn")
        h1 = st.number_input("두 번째 h₁", value=1.0, key="rh1")
        s = st.number_input("두 번째 s", value=0.5, key="rs")
        k = st.number_input("스칼라 k ", value=3.0, key="rgk")
        op = st.selectbox("연산 선택 ", ["원래 등비수열 (g_n)", "스칼라배 (k·g_n)", "두 등비수열의 곱 (g_n · h_n)", "두 등비수열의 나눗셈 (g_n / h_n)"])
        run = st.button("등비 재구성 실행", use_container_width=True)

        if run:
            try:
                res = reconstruct_geometric(op, g1, r, n_terms, k, h1, s)
                n, y = res["n"], res["values"]
                st.latex(res["expr"])
                st.dataframe(pd.DataFrame({"n": n, "재구성 수열": y}).head(10), use_container_width=True)
                if res["new_r"] > 0:
                    x = np.linspace(1, n_terms, 300)
                    y_cont = res["new_g1"] * np.power(res["new_r"], x - 1)
                    animate_sequence_and_function(n, y, x, y_cont, "재구성 점", "대응 지수함수", run_animation=True)
                else:
                    st.warning("새 공비가 0 이하이면 연속 지수함수와 직접 연결하기 어렵습니다.")
                    st.scatter_chart(create_discrete_df(n, y, "재구성 점").set_index("n"), height=320)

                render_result_box([
                    "현재 선택한 재구성 결과는 <b>등비수열</b>입니다.",
                    "대응 함수는 <b>지수함수</b>입니다(공비 양수 조건).",
                    res["why"],
                ])
            except ValueError as e:
                st.error(f"입력값을 확인해 주세요: {e}")
                st.info("정의역 조건을 점검하는 과정 자체가 중요한 수학적 탐구입니다.")


def render_tab_summary() -> None:
    render_explanation_card(
        "학습 정리",
        "수열은 점, 함수는 연속 그래프라는 차이가 있지만 동일한 규칙 구조를 공유할 수 있습니다. "
        "재구성 전후에 무엇이 바뀌고 무엇이 유지되는지 식과 그래프로 함께 설명해 봅시다.",
    )

    st.text_area(
        "무엇을 알게 되었는가?",
        value=(
            "나는 오늘 ________ 수열을 ________ 방식으로 재구성했을 때,\n"
            "새 수열의 일반항이 ________ 꼴이 되어 다시 ________ 함수와 연결된다는 것을 확인했다."
        ),
        height=120,
    )

    st.markdown("#### 수업 마무리 질문")
    st.markdown(
        """
        1. 수열의 점과 함수의 곡선은 무엇이 다르고 무엇이 같은가?
        2. 등차수열의 합/차가 왜 등차수열인지 설명할 수 있는가?
        3. 등비수열 나눗셈에서 정의역 조건은 왜 필요한가?
        4. 공비가 1, 0, 음수일 때 어떤 해석 차이가 생기는가?
        5. 그래프 전개 과정을 보는 것이 식 이해에 어떤 도움을 주는가?
        """
    )

    st.markdown(
        """
        <div class="teacher-box">
            <b>교사용 활용 포인트</b>
            <ul>
                <li>"재구성 전후에 보존되는 구조는 무엇인가?"</li>
                <li>"점(수열)과 연속 그래프(함수)를 어떻게 연결해 설명할 수 있는가?"</li>
                <li>"정의역 조건을 위반하면 어떤 문제가 생기는가?"</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


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

    st.caption("실행 환경에 plotly가 없을 수 있어 Streamlit 기본 차트 기반으로 애니메이션을 구현했습니다.")


if __name__ == "__main__":
    main()

# 실행 방법:
# streamlit run streamlit_app.py
