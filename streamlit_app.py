import importlib
import math
from fractions import Fraction
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

try:
    go = importlib.import_module("plotly.graph_objects")
    pio = importlib.import_module("plotly.io")
    PLOTLY_AVAILABLE = True
except ModuleNotFoundError:
    go = None
    pio = None
    PLOTLY_AVAILABLE = False


st.set_page_config(
    page_title="등차수열과 등비수열의 재구성",
    page_icon="📘",
    layout="wide",
)

# 주요 세션 상태 기본값을 한 번에 초기화한다.
STATE_DEFAULTS: Dict[str, Any] = {
    "cmp_arith_a1": 2.0,
    "cmp_arith_d": 3.0,
    "cmp_arith_n": 8,
    "cmp_arith_drawn": False,
    "cmp_arith_nonce": 0,
    "cmp_geo_g1": 3.0,
    "cmp_geo_r": 1.5,
    "cmp_geo_n": 7,
    "cmp_geo_drawn": False,
    "cmp_geo_nonce": 0,
    "rec_arith_a1": 1.0,
    "rec_arith_d": 2.0,
    "rec_arith_n": 8,
    "rec_arith_b1": 4.0,
    "rec_arith_db": -1.0,
    "rec_arith_k": 2.0,
    "rec_arith_operation": "원래 수열 a_n",
    "rec_arith_drawn": False,
    "rec_arith_nonce": 0,
    "rec_geo_g1": 2.0,
    "rec_geo_r": 2.0,
    "rec_geo_n": 7,
    "rec_geo_h1": 3.0,
    "rec_geo_s": 1.5,
    "rec_geo_k": 2.0,
    "rec_geo_operation": "원래 수열 g_n",
    "rec_geo_drawn": False,
    "rec_geo_nonce": 0,
}


def initialize_session_state() -> None:
    """앱 첫 실행 시 필요한 세션 상태를 채운다."""
    for key, value in STATE_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def inject_css() -> None:
    """글래스모피즘 분위기의 내부 CSS를 주입한다."""
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 12% 10%, rgba(167, 205, 255, 0.55), transparent 22%),
                radial-gradient(circle at 88% 14%, rgba(255, 214, 170, 0.42), transparent 18%),
                linear-gradient(180deg, #f4f8ff 0%, #eef4fb 52%, #e8eef8 100%);
            color: #16314d;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
        }
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }
        .hero-card, .glass-card {
            background:
                linear-gradient(180deg, rgba(255, 255, 255, 0.72), rgba(255, 255, 255, 0.44)),
                linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0));
            border: 1px solid rgba(255, 255, 255, 0.72);
            box-shadow:
                0 18px 44px rgba(63, 93, 135, 0.12),
                inset 0 1px 0 rgba(255, 255, 255, 0.8);
            border-radius: 28px;
            backdrop-filter: blur(18px) saturate(155%);
            -webkit-backdrop-filter: blur(18px) saturate(155%);
        }
        .hero-card {
            padding: 1.8rem 1.9rem;
            margin-bottom: 1.15rem;
        }
        .glass-card {
            padding: 1.15rem 1.25rem;
            margin-bottom: 1rem;
        }
        .hero-title {
            font-size: 2.02rem;
            font-weight: 800;
            color: #142d47;
            margin-bottom: 0.35rem;
            line-height: 1.35;
            letter-spacing: -0.03em;
        }
        .hero-subtitle {
            font-size: 1rem;
            color: #3d5874;
            margin-bottom: 0.9rem;
        }
        .chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        .info-chip {
            display: inline-block;
            padding: 0.42rem 0.9rem;
            border-radius: 999px;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.72), rgba(192, 218, 255, 0.24));
            border: 1px solid rgba(255, 255, 255, 0.78);
            color: #234b73;
            font-size: 0.92rem;
            font-weight: 600;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.58);
        }
        .section-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #16314d;
            margin-bottom: 0.45rem;
            letter-spacing: -0.02em;
        }
        .section-body {
            color: #35516e;
            line-height: 1.7;
            font-size: 0.98rem;
        }
        .summary-title {
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
            color: #16314d;
        }
        .summary-list {
            margin: 0;
            padding-left: 1.2rem;
            color: #35516e;
            line-height: 1.65;
        }
        .small-note {
            color: #59738f;
            font-size: 0.9rem;
        }
        .teacher-prompt {
            background: linear-gradient(155deg, rgba(255, 255, 255, 0.74), rgba(240, 246, 255, 0.48));
            border: 1px solid rgba(255, 255, 255, 0.78);
            border-radius: 22px;
            padding: 0.95rem 1rem;
            margin-bottom: 0.7rem;
            color: #23435f;
            box-shadow: 0 12px 28px rgba(88, 118, 158, 0.09), inset 0 1px 0 rgba(255, 255, 255, 0.78);
        }
        div[data-baseweb="tab-list"] {
            gap: 0.45rem;
            margin-bottom: 0.9rem;
            padding: 0.38rem;
            border-radius: 24px;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.66), rgba(255, 255, 255, 0.38));
            border: 1px solid rgba(255, 255, 255, 0.76);
            box-shadow: 0 12px 28px rgba(88, 118, 158, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.82);
            backdrop-filter: blur(18px) saturate(150%);
            -webkit-backdrop-filter: blur(18px) saturate(150%);
        }
        div[data-baseweb="tab-highlight"] {
            display: none !important;
        }
        button[data-baseweb="tab"] {
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.34) !important;
            border: 1px solid rgba(255, 255, 255, 0.0) !important;
            min-height: 50px;
            padding: 0.56rem 1.04rem 0.76rem 1.04rem !important;
            color: #566b80 !important;
            box-shadow: none !important;
            transition: background 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
        }
        button[data-baseweb="tab"] p,
        button[data-baseweb="tab"] span,
        button[data-baseweb="tab"] div {
            color: #566b80 !important;
            font-weight: 650 !important;
        }
        button[data-baseweb="tab"]:hover {
            background: rgba(255, 255, 255, 0.48) !important;
            border-color: rgba(255, 255, 255, 0.72) !important;
            transform: translateY(-1px);
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            background:
                linear-gradient(180deg, rgba(255, 255, 255, 0.82), rgba(255, 255, 255, 0.54)),
                linear-gradient(90deg, transparent 31%, #ff9e45 31%, #ff9e45 69%, transparent 69%) !important;
            background-repeat: no-repeat, no-repeat !important;
            background-size: 100% 100%, 42% 3px !important;
            background-position: center center, center calc(100% - 7px) !important;
            border-color: rgba(255, 255, 255, 0.82) !important;
            box-shadow:
                0 8px 22px rgba(84, 110, 150, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.92) !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] p,
        button[data-baseweb="tab"][aria-selected="true"] span,
        button[data-baseweb="tab"][aria-selected="true"] div {
            color: #16314d !important;
        }
        .stButton > button {
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.76);
            background:
                linear-gradient(180deg, rgba(255, 255, 255, 0.86), rgba(243, 248, 255, 0.54)),
                linear-gradient(135deg, rgba(122, 169, 255, 0.08), rgba(255, 164, 80, 0.03));
            color: #16314d;
            font-weight: 600;
            box-shadow:
                0 12px 26px rgba(92, 135, 188, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.82);
            transition: all 0.22s ease;
        }
        .stButton > button:hover {
            border-color: rgba(255, 255, 255, 0.86);
            transform: translateY(-1px);
            box-shadow:
                0 16px 32px rgba(92, 135, 188, 0.16),
                inset 0 1px 0 rgba(255, 255, 255, 0.88);
        }
        .stButton > button:focus {
            box-shadow:
                0 0 0 3px rgba(255, 155, 61, 0.16),
                0 16px 32px rgba(92, 135, 188, 0.16),
                inset 0 1px 0 rgba(255, 255, 255, 0.88) !important;
        }
        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        .stNumberInput > div > div,
        .stTextInput > div > div {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.8), rgba(246, 250, 255, 0.56)) !important;
            border: 1px solid rgba(255, 255, 255, 0.76) !important;
            border-radius: 18px !important;
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.88),
                0 10px 24px rgba(90, 124, 168, 0.08) !important;
            backdrop-filter: blur(14px) saturate(150%);
            -webkit-backdrop-filter: blur(14px) saturate(150%);
        }
        .stNumberInput label, .stSelectbox label {
            color: #35516e;
            font-weight: 650;
        }
        div[data-testid="stMetricValue"] {
            color: #16314d;
        }
        div[data-testid="stDataFrame"] {
            border-radius: 24px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.74);
            box-shadow:
                0 16px 36px rgba(80, 118, 168, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.78);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
        }
        div[data-testid="stAlert"] {
            border-radius: 22px;
            border: 1px solid rgba(255, 255, 255, 0.74);
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.82), rgba(247, 250, 255, 0.48));
            box-shadow: 0 12px 28px rgba(88, 118, 158, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.84);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    """상단 제목과 선행조직자 역할을 하는 안내를 그린다."""
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">등차수열과 등비수열의 재구성: 함수와 연결하여 이해하기</div>
            <div class="hero-subtitle">수열의 점과 함수의 그래프를 비교하며 규칙의 구조를 탐구하는 수업용 앱</div>
            <div class="chip-row">
                <span class="info-chip">등차수열은 자연수에서 정의된 일차적 규칙</span>
                <span class="info-chip">등비수열은 자연수에서 정의된 지수적 규칙</span>
                <span class="info-chip">수열은 점, 함수는 연속 그래프</span>
                <span class="info-chip">규칙의 구조는 서로 연결 가능</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_summary_card(title: str, lines: list[str]) -> None:
    """짧은 요약을 담는 카드형 박스를 표시한다."""
    line_html = "".join(f"<li>{line}</li>" for line in lines)
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="summary-title">{title}</div>
            <ul class="summary-list">{line_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_number(value: float) -> str:
    """표와 설명에 쓰기 좋은 숫자 문자열로 바꾼다."""
    if value is None or not np.isfinite(value):
        return "정의되지 않음"
    if math.isclose(value, 0.0, abs_tol=1e-10):
        return "0"
    if math.isclose(value, round(value), abs_tol=1e-10):
        return str(int(round(value)))
    abs_value = abs(value)
    if abs_value >= 1_000_000 or (0 < abs_value < 0.0001):
        return f"{value:.3e}"
    return f"{value:.4f}".rstrip("0").rstrip(".")


def is_close_zero(value: float) -> bool:
    """거의 0인지 판별한다."""
    return math.isclose(value, 0.0, abs_tol=1e-10)


def is_close_one(value: float) -> bool:
    """거의 1인지 판별한다."""
    return math.isclose(value, 1.0, abs_tol=1e-10)


def format_latex_number(value: float) -> str:
    """LaTeX 표시에 적절한 숫자 문자열을 만든다."""
    if value is None or not np.isfinite(value):
        return r"\text{정의되지 않음}"
    if is_close_zero(value):
        return "0"
    fraction = Fraction(value).limit_denominator(1000)
    if abs(float(fraction) - value) < 1e-10:
        if fraction.denominator == 1:
            return str(fraction.numerator)
        return rf"\frac{{{fraction.numerator}}}{{{fraction.denominator}}}"
    return format_number(value)


def format_power_base_latex(value: float) -> str:
    """지수의 밑으로 쓸 숫자를 LaTeX로 안전하게 만든다."""
    base = format_latex_number(value)
    if "\\" in base or value < 0 or not math.isclose(value, round(value), abs_tol=1e-10):
        return rf"\left({base}\right)"
    return base


def format_coefficient_text(coefficient: float, token: str) -> str:
    """선형식 항의 텍스트 계수를 만든다."""
    if is_close_zero(coefficient):
        return "0"
    if is_close_one(coefficient):
        return token
    if math.isclose(coefficient, -1.0, abs_tol=1e-10):
        return f"-{token}"
    return f"{format_number(coefficient)}{token}"


def format_coefficient_latex(coefficient: float, token: str) -> str:
    """선형식 항의 LaTeX 계수를 만든다."""
    if is_close_zero(coefficient):
        return "0"
    if is_close_one(coefficient):
        return token
    if math.isclose(coefficient, -1.0, abs_tol=1e-10):
        return f"-{token}"
    return rf"{format_latex_number(coefficient)}{token}"


def arithmetic_expr_text(a1: float, d: float, variable: str = "n") -> str:
    """등차수열 또는 대응 함수의 식을 텍스트로 만든다."""
    if is_close_zero(d):
        return format_number(a1)
    token = f"({variable}-1)"
    if is_close_zero(a1):
        return format_coefficient_text(d, token)
    sign = "+" if d > 0 else "-"
    return f"{format_number(a1)} {sign} {format_coefficient_text(abs(d), token)}"


def arithmetic_expr_latex(a1: float, d: float, variable: str = "n") -> str:
    """등차수열 또는 대응 함수의 식을 LaTeX로 만든다."""
    if is_close_zero(d):
        return format_latex_number(a1)
    token = rf"\left({variable}-1\right)"
    if is_close_zero(a1):
        return format_coefficient_latex(d, token)
    sign = "+" if d > 0 else "-"
    return rf"{format_latex_number(a1)} {sign} {format_coefficient_latex(abs(d), token)}"


def geometric_expr_text(g1: float, r: float, variable: str = "n") -> str:
    """등비수열 또는 대응 함수의 식을 텍스트로 만든다."""
    if is_close_zero(g1):
        return "0"
    if is_close_one(r):
        return format_number(g1)
    base = format_number(r)
    if (not math.isclose(r, round(r), abs_tol=1e-10)) or r < 0:
        base = f"({base})"
    power = f"{base}^({variable}-1)"
    if is_close_one(g1):
        return power
    if math.isclose(g1, -1.0, abs_tol=1e-10):
        return f"-{power}"
    return f"{format_number(g1)}·{power}"


def geometric_expr_latex(g1: float, r: float, variable: str = "n") -> str:
    """등비수열 또는 대응 함수의 식을 LaTeX로 만든다."""
    if is_close_zero(g1):
        return "0"
    if is_close_one(r):
        return format_latex_number(g1)
    power = rf"{format_power_base_latex(r)}^{{{variable}-1}}"
    if is_close_one(g1):
        return power
    if math.isclose(g1, -1.0, abs_tol=1e-10):
        return rf"-{power}"
    return rf"{format_latex_number(g1)} \cdot {power}"


def arithmetic_sequence(a1: float, d: float, count: int) -> Tuple[np.ndarray, np.ndarray]:
    """등차수열의 항 번호와 값을 생성한다."""
    indices = np.arange(1, count + 1, dtype=float)
    values = a1 + (indices - 1) * d
    return indices, values.astype(float)


def geometric_sequence(g1: float, r: float, count: int) -> Tuple[np.ndarray, np.ndarray]:
    """등비수열의 항 번호와 값을 생성한다."""
    indices = np.arange(1, count + 1, dtype=float)
    with np.errstate(over="ignore", invalid="ignore"):
        values = g1 * np.power(r, indices - 1)
    return indices, values.astype(float)


def make_term_dataframe(indices: np.ndarray, values: np.ndarray, column_name: str) -> pd.DataFrame:
    """수열의 앞부분 항을 표로 정리한다."""
    return pd.DataFrame(
        {
            "항 번호": [int(x) for x in indices],
            column_name: [format_number(v) for v in values],
        }
    )


def build_message_figure(title: str, message: str) -> Any:
    """입력 전 또는 오류 상황에서 안내용 빈 그래프를 만든다."""
    if not PLOTLY_AVAILABLE:
        return None
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=16, color="#35516e"),
    )
    fig.update_layout(
        title=title,
        height=470,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.7)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=30, r=30, t=70, b=30),
    )
    return fig


def validate_finite_values(values: np.ndarray) -> bool:
    """그래프에 표시 가능한 유한한 값인지 검사한다."""
    return bool(np.all(np.isfinite(values)))


def compute_y_range(point_values: np.ndarray, curve_values: np.ndarray) -> Tuple[float, float]:
    """그래프의 y축 범위를 적절히 잡는다."""
    all_values = np.concatenate([point_values, curve_values])
    finite_values = all_values[np.isfinite(all_values)]
    if finite_values.size == 0:
        return -1.0, 1.0
    min_value = float(np.min(finite_values))
    max_value = float(np.max(finite_values))
    if math.isclose(min_value, max_value, abs_tol=1e-10):
        padding = max(1.0, abs(min_value) * 0.2 + 1.0)
        return min_value - padding, max_value + padding
    padding = (max_value - min_value) * 0.15
    return min_value - padding, max_value + padding


def build_animated_plot(
    point_x: np.ndarray,
    point_y: np.ndarray,
    curve_x: np.ndarray,
    curve_y: np.ndarray,
    title: str,
    point_label: str,
    curve_label: str,
) -> Any:
    """Plotly 프레임을 사용해 왼쪽에서 오른쪽으로 그려지는 그래프를 만든다."""
    if not PLOTLY_AVAILABLE:
        return None
    if len(point_x) == 0 or len(curve_x) == 0:
        return build_message_figure(title, "그래프를 만들 데이터가 아직 없습니다.")

    animation_frame_ms = 23
    animation_transition_ms = 9
    point_count = len(point_x)
    curve_count = len(curve_x)
    frame_count = max(20, min(42, max(curve_count // 5, point_count * 2)))
    y_min, y_max = compute_y_range(point_y, curve_y)
    first_curve_index = max(3, int(math.ceil(curve_count / frame_count)))
    first_point_index = 1

    fig = go.Figure(
        data=[
            go.Scatter(
                x=curve_x[:first_curve_index],
                y=curve_y[:first_curve_index],
                mode="lines",
                line=dict(color="#5B8DEF", width=4),
                name=curve_label,
            ),
            go.Scatter(
                x=point_x[:first_point_index],
                y=point_y[:first_point_index],
                mode="markers",
                marker=dict(size=11, color="#143d67", line=dict(color="#ffffff", width=1.8)),
                name=point_label,
            ),
        ]
    )

    frames = []
    for frame_index in range(1, frame_count + 1):
        fraction = frame_index / frame_count
        curve_end = max(2, min(curve_count, int(math.ceil(curve_count * fraction))))
        point_end = max(1, min(point_count, int(math.ceil(point_count * fraction))))
        frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=curve_x[:curve_end],
                        y=curve_y[:curve_end],
                        mode="lines",
                        line=dict(color="#5B8DEF", width=4),
                        name=curve_label,
                    ),
                    go.Scatter(
                        x=point_x[:point_end],
                        y=point_y[:point_end],
                        mode="markers",
                        marker=dict(size=11, color="#143d67", line=dict(color="#ffffff", width=1.8)),
                        name=point_label,
                    ),
                ],
                name=f"frame_{frame_index}",
            )
        )
    fig.frames = frames

    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color="#17324d")),
        height=520,
        margin=dict(l=30, r=30, t=80, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.78)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.0)",
        ),
        xaxis=dict(
            title="항 번호 / 연속 변수 x",
            range=[0.8, float(max(point_x.max(), curve_x.max())) + 0.2],
            gridcolor="rgba(130, 166, 211, 0.22)",
            zeroline=False,
        ),
        yaxis=dict(
            title="값",
            range=[y_min, y_max],
            gridcolor="rgba(130, 166, 211, 0.22)",
            zeroline=False,
        ),
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                x=0.0,
                y=1.18,
                showactive=False,
                bgcolor="rgba(255,255,255,0.72)",
                bordercolor="rgba(130, 166, 211, 0.2)",
                buttons=[
                    dict(
                        label="재생",
                        method="animate",
                        args=[
                            None,
                            {
                                "frame": {"duration": animation_frame_ms, "redraw": False},
                                "transition": {"duration": animation_transition_ms, "easing": "linear"},
                                "fromcurrent": True,
                                "mode": "immediate",
                            },
                        ],
                    ),
                    dict(
                        label="일시정지",
                        method="animate",
                        args=[
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "transition": {"duration": 0, "easing": "linear"},
                                "mode": "immediate",
                            },
                        ],
                    ),
                    dict(
                        label="처음으로",
                        method="animate",
                        args=[
                            ["frame_1"],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "transition": {"duration": 0, "easing": "linear"},
                                "mode": "immediate",
                            },
                        ],
                    ),
                ],
            )
        ],
    )
    return fig


def render_plotly_animation(fig: Any, chart_id: str, nonce: int) -> None:
    """Plotly HTML을 직접 렌더링해 자동 재생되는 애니메이션을 표시한다."""
    if not PLOTLY_AVAILABLE or fig is None:
        st.warning("현재 Python 환경에서 `plotly`를 찾지 못해 그래프를 표시할 수 없습니다. `pip install plotly` 후 다시 실행하면 그래프가 정상적으로 나타납니다.")
        return
    html = pio.to_html(
        fig,
        include_plotlyjs=True,
        full_html=False,
        auto_play=True,
        div_id=f"{chart_id}_{nonce}",
    )
    html += f"<!-- animation-{chart_id}-{nonce} -->"
    components.html(html, height=int(fig.layout.height or 520) + 20, scrolling=False)


def reconstruct_arithmetic(
    a1: float,
    d: float,
    count: int,
    operation: str,
    b1: float,
    db: float,
    k: float,
) -> Dict[str, Any]:
    """등차수열 재구성 결과를 수학적으로 계산한다."""
    if operation == "원래 수열 a_n":
        new_first = a1
        new_diff = d
        explanation = "공차가 일정하므로 원래 수열 자체가 등차수열입니다."
    elif operation == "스칼라배 k·a_n":
        new_first = k * a1
        new_diff = k * d
        explanation = "모든 항에 같은 수를 곱하면 인접한 항의 차도 같은 배수만큼 바뀌므로 공차가 일정하게 유지됩니다."
    elif operation == "두 등차수열의 합 a_n + b_n":
        new_first = a1 + b1
        new_diff = d + db
        explanation = "두 수열의 n번째 항을 더하면 첫째항은 더해지고 공차도 더해져 다시 등차수열이 됩니다."
    else:
        new_first = a1 - b1
        new_diff = d - db
        explanation = "두 수열의 n번째 항을 빼면 첫째항은 차가 되고 공차도 차가 되어 다시 등차수열이 됩니다."

    indices, values = arithmetic_sequence(new_first, new_diff, count)
    result = {
        "valid": True,
        "new_first": new_first,
        "new_diff": new_diff,
        "indices": indices,
        "values": values,
        "sequence_expr": arithmetic_expr_text(new_first, new_diff),
        "sequence_latex": arithmetic_expr_latex(new_first, new_diff),
        "function_expr": arithmetic_expr_text(new_first, new_diff, variable="x"),
        "function_latex": arithmetic_expr_latex(new_first, new_diff, variable="x"),
        "explanation": explanation,
    }
    return result


def reconstruct_geometric(
    g1: float,
    r: float,
    count: int,
    operation: str,
    h1: float,
    s: float,
    k: float,
) -> Dict[str, Any]:
    """등비수열 재구성 결과를 수학적으로 계산한다."""
    if r <= 0:
        return {
            "valid": False,
            "message": "이 앱에서는 등비수열을 지수함수와 연결하기 위해 공비를 양수로 둡니다. 0 이하의 공비는 연속 그래프로 자연스럽게 잇기 어려우므로 양수를 입력해 주세요.",
        }
    if operation in {"두 등비수열의 곱 g_n · h_n", "두 등비수열의 나눗셈 g_n / h_n"} and s <= 0:
        return {
            "valid": False,
            "message": "보조 등비수열도 지수함수와 연결하려면 공비를 양수로 두는 것이 좋습니다. s를 양수로 다시 입력해 주세요.",
        }

    ratio_note = ""
    if operation == "원래 수열 g_n":
        new_first = g1
        new_ratio = r
        explanation = "공비가 일정하므로 원래 수열 자체가 등비수열입니다."
    elif operation == "스칼라배 k·g_n":
        new_first = k * g1
        new_ratio = r
        if math.isclose(k, 0.0, abs_tol=1e-10):
            explanation = "모든 항이 0인 영수열이 됩니다. 0·r^(n-1)=0 꼴로 쓸 수 있어 같은 형태로 볼 수 있지만, 공비는 하나로만 정해지지 않는다는 점을 함께 생각해 볼 수 있습니다."
            ratio_note = "영수열이라 공비가 하나로 유일하게 정해지지는 않습니다."
        else:
            explanation = "모든 항에 같은 상수를 곱해도 인접한 두 항의 비는 그대로 유지되므로 다시 등비수열입니다."
    elif operation == "두 등비수열의 곱 g_n · h_n":
        new_first = g1 * h1
        new_ratio = r * s
        explanation = "각 항을 곱하면 첫째항은 g1·h1, 공비는 r·s가 되어 다시 등비수열이 됩니다."
    else:
        h_indices, h_values = geometric_sequence(h1, s, count)
        if not validate_finite_values(h_values):
            return {
                "valid": False,
                "message": "보조 등비수열의 값이 너무 커져서 나눗셈을 안정적으로 표시하기 어렵습니다. 항의 개수나 공비를 조금 줄여 보세요.",
            }
        if np.any(np.isclose(h_values, 0.0, atol=1e-12)):
            return {
                "valid": False,
                "message": "나눗셈 재구성에서는 분모 수열 h_n이 0이 되면 항을 만들 수 없습니다. h1과 s를 다시 확인해 주세요.",
            }
        new_first = g1 / h1
        new_ratio = r / s
        explanation = "각 항을 나누면 첫째항은 g1/h1, 공비는 r/s가 되어 다시 등비수열이 됩니다. 단, 모든 h_n이 0이 아니어야 합니다."

    indices, values = geometric_sequence(new_first, new_ratio, count)
    result = {
        "valid": True,
        "new_first": new_first,
        "new_ratio": new_ratio,
        "indices": indices,
        "values": values,
        "sequence_expr": geometric_expr_text(new_first, new_ratio),
        "sequence_latex": geometric_expr_latex(new_first, new_ratio),
        "function_expr": geometric_expr_text(new_first, new_ratio, variable="x"),
        "function_latex": geometric_expr_latex(new_first, new_ratio, variable="x"),
        "explanation": explanation,
        "ratio_note": ratio_note,
    }
    return result


def load_arithmetic_compare_example(example_no: int) -> None:
    """등차수열 비교 탐구 예시를 불러온다."""
    if example_no == 1:
        st.session_state["cmp_arith_a1"] = 2.0
        st.session_state["cmp_arith_d"] = 3.0
        st.session_state["cmp_arith_n"] = 8
    else:
        st.session_state["cmp_arith_a1"] = 10.0
        st.session_state["cmp_arith_d"] = -2.0
        st.session_state["cmp_arith_n"] = 9
    st.session_state["cmp_arith_drawn"] = False
    st.session_state["cmp_arith_nonce"] += 1


def load_geometric_compare_example(example_no: int) -> None:
    """등비수열 비교 탐구 예시를 불러온다."""
    if example_no == 1:
        st.session_state["cmp_geo_g1"] = 3.0
        st.session_state["cmp_geo_r"] = 2.0
        st.session_state["cmp_geo_n"] = 7
    else:
        st.session_state["cmp_geo_g1"] = 81.0
        st.session_state["cmp_geo_r"] = 0.5
        st.session_state["cmp_geo_n"] = 8
    st.session_state["cmp_geo_drawn"] = False
    st.session_state["cmp_geo_nonce"] += 1


def load_arithmetic_reconstruction_example(example_no: int) -> None:
    """등차수열 재구성 예시를 불러온다."""
    if example_no == 1:
        st.session_state["rec_arith_a1"] = 1.0
        st.session_state["rec_arith_d"] = 2.0
        st.session_state["rec_arith_b1"] = 4.0
        st.session_state["rec_arith_db"] = -1.0
        st.session_state["rec_arith_k"] = 3.0
        st.session_state["rec_arith_n"] = 8
        st.session_state["rec_arith_operation"] = "두 등차수열의 합 a_n + b_n"
    else:
        st.session_state["rec_arith_a1"] = 7.0
        st.session_state["rec_arith_d"] = 0.0
        st.session_state["rec_arith_b1"] = 2.0
        st.session_state["rec_arith_db"] = 3.0
        st.session_state["rec_arith_k"] = -2.0
        st.session_state["rec_arith_n"] = 7
        st.session_state["rec_arith_operation"] = "스칼라배 k·a_n"
    st.session_state["rec_arith_drawn"] = False
    st.session_state["rec_arith_nonce"] += 1


def load_geometric_reconstruction_example(example_no: int) -> None:
    """등비수열 재구성 예시를 불러온다."""
    if example_no == 1:
        st.session_state["rec_geo_g1"] = 2.0
        st.session_state["rec_geo_r"] = 2.0
        st.session_state["rec_geo_h1"] = 3.0
        st.session_state["rec_geo_s"] = 1.5
        st.session_state["rec_geo_k"] = 2.0
        st.session_state["rec_geo_n"] = 7
        st.session_state["rec_geo_operation"] = "두 등비수열의 곱 g_n · h_n"
    else:
        st.session_state["rec_geo_g1"] = 64.0
        st.session_state["rec_geo_r"] = 0.5
        st.session_state["rec_geo_h1"] = 4.0
        st.session_state["rec_geo_s"] = 2.0
        st.session_state["rec_geo_k"] = 0.0
        st.session_state["rec_geo_n"] = 7
        st.session_state["rec_geo_operation"] = "스칼라배 k·g_n"
    st.session_state["rec_geo_drawn"] = False
    st.session_state["rec_geo_nonce"] += 1


def render_concept_tab() -> None:
    """개념 연결 탭을 그린다."""
    col1, col2 = st.columns([1.15, 1.0], gap="large")
    with col1:
        render_summary_card(
            "선행조직자",
            [
                "등차수열은 항 번호가 1씩 증가할 때 값이 일정하게 변하므로 자연수에서 정의된 일차적 규칙으로 볼 수 있습니다.",
                "등비수열은 항 번호가 1씩 증가할 때 값이 일정한 비율로 변하므로 지수적 규칙으로 이해할 수 있습니다.",
                "수열은 점으로, 함수는 연속 그래프로 나타나지만 규칙의 구조는 서로 연결될 수 있습니다.",
            ],
        )
        render_summary_card(
            "오늘의 학습 흐름",
            [
                "먼저 수열의 점과 함수 그래프를 비교하여 규칙의 닮은 점을 확인합니다.",
                "그다음 덧셈, 뺄셈, 곱셈, 나눗셈, 스칼라배로 수열을 재구성해 봅니다.",
                "마지막에는 재구성한 결과도 같은 유형의 규칙인지 스스로 설명해 봅니다.",
            ],
        )
    with col2:
        render_summary_card(
            "통합적 조정",
            [
                "수열은 이산적 점이라서 항 번호가 자연수일 때만 나타납니다.",
                "함수는 연속 그래프라서 중간의 x값까지 함께 해석할 수 있습니다.",
                "표현 방식은 다르지만 규칙의 변화 구조는 서로 이어서 생각할 수 있습니다.",
            ],
        )
        render_summary_card(
            "능동적 의미 형성",
            [
                "값을 직접 입력하고 그래프를 그려 보세요.",
                "재구성 전후의 식과 그래프를 비교하며 규칙이 어떻게 바뀌는지 확인해 보세요.",
                "교사용 발문을 바탕으로 친구와 설명을 나눠 보세요.",
            ],
        )

    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">수업 관찰 포인트</div>
            <div class="section-body">
                등차수열의 점들이 일차함수 위에 놓이는지, 등비수열의 점들이 지수함수적 패턴을 따르는지 관찰해 보세요.
                특히 수열은 점으로만 찍히고 함수는 연속 곡선으로 이어진다는 차이를 의식하면, 같은 규칙 구조를 다른 표현으로 읽는 경험을 만들 수 있습니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_arithmetic_compare_section() -> None:
    """등차수열과 일차함수 비교 탐구를 렌더링한다."""
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">등차수열과 일차함수 비교</div>
            <div class="section-body">
                등차수열은 항 번호가 1씩 증가할 때 값이 일정하게 변합니다.
                그래서 자연수에서 정의된 일차적 규칙으로 이해할 수 있고, 그 점들은 대응하는 일차함수 위에 놓이게 됩니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    example_cols = st.columns(3)
    with example_cols[0]:
        st.markdown("**예시 불러오기**")
    with example_cols[1]:
        if st.button("예시 1: 증가", key="cmp_arith_ex1"):
            load_arithmetic_compare_example(1)
    with example_cols[2]:
        if st.button("예시 2: 감소", key="cmp_arith_ex2"):
            load_arithmetic_compare_example(2)

    col1, col2, col3 = st.columns(3)
    with col1:
        a1 = float(st.number_input("첫째항 a1", key="cmp_arith_a1", step=1.0))
    with col2:
        d = float(st.number_input("공차 d", key="cmp_arith_d", step=1.0))
    with col3:
        count = int(st.number_input("항의 개수 n", min_value=2, max_value=30, key="cmp_arith_n", step=1))

    st.latex(r"a_n = a_1 + (n-1)d")
    st.latex(r"y = a_1 + (x-1)d")
    st.latex(rf"a_n = {arithmetic_expr_latex(a1, d)}")
    st.latex(rf"y = {arithmetic_expr_latex(a1, d, variable='x')}")

    indices, values = arithmetic_sequence(a1, d, count)
    curve_x = np.linspace(1, max(count, 2), 220)
    curve_y = a1 + (curve_x - 1) * d

    button_cols = st.columns([1, 1, 3])
    with button_cols[0]:
        if st.button("그래프 그리기", key="cmp_arith_draw"):
            st.session_state["cmp_arith_drawn"] = True
    with button_cols[1]:
        if st.button("애니메이션 다시 보기", key="cmp_arith_replay"):
            st.session_state["cmp_arith_drawn"] = True
            st.session_state["cmp_arith_nonce"] += 1

    if not validate_finite_values(values) or not validate_finite_values(curve_y):
        st.warning("값의 크기가 너무 커서 그래프를 안정적으로 나타내기 어렵습니다. 공차나 항의 개수를 조금 줄여 보세요.")
        fig = build_message_figure("등차수열 비교 그래프", "입력값을 조금 조정하면 그래프를 더 선명하게 비교할 수 있습니다.")
        render_plotly_animation(fig, "cmp_arith_message", st.session_state["cmp_arith_nonce"])
    elif st.session_state["cmp_arith_drawn"]:
        fig = build_animated_plot(
            indices,
            values,
            curve_x,
            curve_y,
            "등차수열의 점과 일차함수의 그래프",
            "수열의 점",
            "대응하는 일차함수",
        )
        render_plotly_animation(fig, "cmp_arith_chart", st.session_state["cmp_arith_nonce"])
        st.caption("그래프가 열리면 애니메이션이 자동 재생됩니다. 다시 보고 싶으면 위의 버튼을 눌러 보세요.")
    else:
        st.info("`그래프 그리기`를 누르면 수열의 점과 대응하는 일차함수가 함께 나타납니다.")

    preview_count = min(8, count)
    st.dataframe(
        make_term_dataframe(indices[:preview_count], values[:preview_count], "a_n"),
        use_container_width=True,
        hide_index=True,
    )

    interpretation = (
        "공차가 0이므로 값이 일정한 상수 수열이며, 그래프는 수평선 위의 점들로 보입니다."
        if math.isclose(d, 0.0, abs_tol=1e-10)
        else "항 번호가 1 늘 때마다 값이 일정하게 변하므로 점들이 하나의 직선 위에 놓입니다."
    )
    render_summary_card(
        "결과 요약",
        [
            f"일반항: a_n = {arithmetic_expr_text(a1, d)}",
            f"처음 몇 개 항: {', '.join(format_number(v) for v in values[:preview_count])}",
            interpretation,
            "수열은 점으로 찍히지만, 그 점들은 대응하는 일차함수 위에 놓입니다.",
        ],
    )


def render_geometric_compare_section() -> None:
    """등비수열과 지수함수 비교 탐구를 렌더링한다."""
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">등비수열과 지수함수 비교</div>
            <div class="section-body">
                등비수열은 항 번호가 1씩 증가할 때 값이 일정한 비율로 변합니다.
                그래서 자연수에서 정의된 지수적 규칙으로 볼 수 있고, 그 점들은 대응하는 지수함수적 패턴 위에 놓입니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    example_cols = st.columns(3)
    with example_cols[0]:
        st.markdown("**예시 불러오기**")
    with example_cols[1]:
        if st.button("예시 1: 성장", key="cmp_geo_ex1"):
            load_geometric_compare_example(1)
    with example_cols[2]:
        if st.button("예시 2: 감소", key="cmp_geo_ex2"):
            load_geometric_compare_example(2)

    col1, col2, col3 = st.columns(3)
    with col1:
        g1 = float(st.number_input("첫째항 g1", key="cmp_geo_g1", step=1.0))
    with col2:
        r = float(st.number_input("공비 r", key="cmp_geo_r", step=0.1))
    with col3:
        count = int(st.number_input("항의 개수 n", min_value=2, max_value=20, key="cmp_geo_n", step=1))

    st.latex(r"g_n = g_1 \cdot r^{n-1}")
    st.latex(r"y = g_1 \cdot r^{x-1}")

    button_cols = st.columns([1, 1, 3])
    with button_cols[0]:
        if st.button("그래프 그리기", key="cmp_geo_draw"):
            st.session_state["cmp_geo_drawn"] = True
    with button_cols[1]:
        if st.button("애니메이션 다시 보기", key="cmp_geo_replay"):
            st.session_state["cmp_geo_drawn"] = True
            st.session_state["cmp_geo_nonce"] += 1

    if r <= 0:
        st.warning("이 앱에서는 등비수열을 지수함수와 자연스럽게 연결하기 위해 공비를 양수로 둡니다. 0 이하의 공비는 연속 그래프로 같은 방식으로 이어 보기 어렵습니다.")
        fig = build_message_figure("등비수열 비교 그래프", "공비 r를 양수로 입력하면 지수함수와의 연결을 확인할 수 있습니다.")
        render_plotly_animation(fig, "cmp_geo_invalid", st.session_state["cmp_geo_nonce"])
        return

    indices, values = geometric_sequence(g1, r, count)
    curve_x = np.linspace(1, max(count, 2), 240)
    with np.errstate(over="ignore", invalid="ignore"):
        curve_y = g1 * np.power(r, curve_x - 1)

    st.latex(rf"g_n = {geometric_expr_latex(g1, r)}")
    st.latex(rf"y = {geometric_expr_latex(g1, r, variable='x')}")

    if not validate_finite_values(values) or not validate_finite_values(curve_y):
        st.error("값의 크기가 너무 커서 그래프를 안정적으로 표시하기 어렵습니다. 공비나 항의 개수를 조금 줄여 보세요.")
        fig = build_message_figure("등비수열 비교 그래프", "입력값을 조정하면 지수적 패턴을 더 분명하게 확인할 수 있습니다.")
        render_plotly_animation(fig, "cmp_geo_message", st.session_state["cmp_geo_nonce"])
    elif st.session_state["cmp_geo_drawn"]:
        fig = build_animated_plot(
            indices,
            values,
            curve_x,
            curve_y,
            "등비수열의 점과 지수함수의 그래프",
            "수열의 점",
            "대응하는 지수함수",
        )
        render_plotly_animation(fig, "cmp_geo_chart", st.session_state["cmp_geo_nonce"])
        st.caption("그래프는 자동으로 재생됩니다. 공비가 1이면 상수 함수와 같은 모습이 나타납니다.")
    else:
        st.info("`그래프 그리기`를 누르면 수열의 점과 대응하는 지수함수적 패턴이 함께 나타납니다.")

    preview_count = min(8, count)
    st.dataframe(
        make_term_dataframe(indices[:preview_count], values[:preview_count], "g_n"),
        use_container_width=True,
        hide_index=True,
    )

    interpretation = (
        "공비가 1이므로 모든 항이 같아지고, 지수함수 그래프도 수평선처럼 보입니다."
        if math.isclose(r, 1.0, abs_tol=1e-10)
        else "항 번호가 1 늘 때마다 값이 일정한 비율로 변하므로 점들이 지수함수적 패턴 위에 놓입니다."
    )
    render_summary_card(
        "결과 요약",
        [
            f"일반항: g_n = {geometric_expr_text(g1, r)}",
            f"처음 몇 개 항: {', '.join(format_number(v) for v in values[:preview_count])}",
            interpretation,
            "수열은 점으로만 나타나지만, 규칙의 구조는 연속적인 지수함수와 연결해 볼 수 있습니다.",
        ],
    )


def render_arithmetic_reconstruction_section() -> None:
    """등차수열 재구성 실험을 렌더링한다."""
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">등차수열 재구성 실험</div>
            <div class="section-body">
                덧셈, 뺄셈, 스칼라배로 수열을 바꾸어도 다시 등차수열이 되는지 확인해 봅시다.
                식과 그래프를 함께 보면 왜 같은 유형의 규칙이 유지되는지 더 분명하게 볼 수 있습니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    example_cols = st.columns(3)
    with example_cols[0]:
        st.markdown("**예시 불러오기**")
    with example_cols[1]:
        if st.button("예시 1: 합", key="rec_arith_ex1"):
            load_arithmetic_reconstruction_example(1)
    with example_cols[2]:
        if st.button("예시 2: 상수수열", key="rec_arith_ex2"):
            load_arithmetic_reconstruction_example(2)

    row1 = st.columns(4)
    with row1[0]:
        a1 = float(st.number_input("첫째항 a1", key="rec_arith_a1", step=1.0))
    with row1[1]:
        d = float(st.number_input("공차 d", key="rec_arith_d", step=1.0))
    with row1[2]:
        count = int(st.number_input("항의 개수 n", min_value=2, max_value=25, key="rec_arith_n", step=1))
    with row1[3]:
        k = float(st.number_input("스칼라 k", key="rec_arith_k", step=1.0))

    row2 = st.columns(3)
    with row2[0]:
        operation = st.selectbox(
            "재구성 방식",
            [
                "원래 수열 a_n",
                "스칼라배 k·a_n",
                "두 등차수열의 합 a_n + b_n",
                "두 등차수열의 차 a_n - b_n",
            ],
            key="rec_arith_operation",
        )
    with row2[1]:
        b1 = float(st.number_input("둘째 수열의 첫째항 b1", key="rec_arith_b1", step=1.0))
    with row2[2]:
        db = float(st.number_input("둘째 수열의 공차 db", key="rec_arith_db", step=1.0))

    result = reconstruct_arithmetic(a1, d, count, operation, b1, db, k)
    preview_count = min(8, count)

    st.latex(r"a_n = a_1 + (n-1)d")
    st.latex(r"b_n = b_1 + (n-1)d_b")
    st.latex(rf"u_n = {result['sequence_latex']}")
    st.latex(rf"y = {result['function_latex']}")

    button_cols = st.columns([1, 1, 3])
    with button_cols[0]:
        if st.button("그래프 그리기", key="rec_arith_draw"):
            st.session_state["rec_arith_drawn"] = True
    with button_cols[1]:
        if st.button("애니메이션 다시 보기", key="rec_arith_replay"):
            st.session_state["rec_arith_drawn"] = True
            st.session_state["rec_arith_nonce"] += 1

    if not validate_finite_values(result["values"]):
        st.warning("재구성한 값의 크기가 너무 커서 그래프를 안정적으로 표현하기 어렵습니다. 입력값을 조금 줄여 보세요.")
        fig = build_message_figure("등차수열 재구성 그래프", "입력값을 조정하면 재구성 결과를 더 선명하게 볼 수 있습니다.")
        render_plotly_animation(fig, "rec_arith_invalid", st.session_state["rec_arith_nonce"])
    elif st.session_state["rec_arith_drawn"]:
        curve_x = np.linspace(1, max(count, 2), 220)
        curve_y = result["new_first"] + (curve_x - 1) * result["new_diff"]
        fig = build_animated_plot(
            result["indices"],
            result["values"],
            curve_x,
            curve_y,
            "재구성한 등차수열과 대응하는 일차함수",
            "재구성한 수열의 점",
            "대응하는 일차함수",
        )
        render_plotly_animation(fig, "rec_arith_chart", st.session_state["rec_arith_nonce"])
    else:
        st.info("재구성 방식을 고른 뒤 `그래프 그리기`를 눌러 식과 그래프를 함께 확인해 보세요.")

    st.dataframe(
        make_term_dataframe(result["indices"][:preview_count], result["values"][:preview_count], "u_n"),
        use_container_width=True,
        hide_index=True,
    )

    render_summary_card(
        "재구성 결과",
        [
            f"새 수열의 일반항: u_n = {result['sequence_expr']}",
            f"처음 몇 개 항: {', '.join(format_number(v) for v in result['values'][:preview_count])}",
            f"첫째항과 공차: ({format_number(result['new_first'])}, {format_number(result['new_diff'])})",
            result["explanation"],
            "재구성한 점들도 다시 하나의 직선 위에 놓이는지 그래프에서 확인해 보세요.",
        ],
    )


def render_geometric_reconstruction_section() -> None:
    """등비수열 재구성 실험을 렌더링한다."""
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">등비수열 재구성 실험</div>
            <div class="section-body">
                곱셈, 나눗셈, 스칼라배로 수열을 바꾼 뒤에도 다시 등비수열이 되는지 확인해 봅시다.
                연속적인 지수함수와 연결하기 위해 이 앱에서는 공비를 양수로 두고 탐구합니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    example_cols = st.columns(3)
    with example_cols[0]:
        st.markdown("**예시 불러오기**")
    with example_cols[1]:
        if st.button("예시 1: 곱셈", key="rec_geo_ex1"):
            load_geometric_reconstruction_example(1)
    with example_cols[2]:
        if st.button("예시 2: 영수열", key="rec_geo_ex2"):
            load_geometric_reconstruction_example(2)

    row1 = st.columns(4)
    with row1[0]:
        g1 = float(st.number_input("첫째항 g1", key="rec_geo_g1", step=1.0))
    with row1[1]:
        r = float(st.number_input("공비 r", key="rec_geo_r", step=0.1))
    with row1[2]:
        count = int(st.number_input("항의 개수 n", min_value=2, max_value=16, key="rec_geo_n", step=1))
    with row1[3]:
        k = float(st.number_input("스칼라 k", key="rec_geo_k", step=0.5))

    row2 = st.columns(3)
    with row2[0]:
        operation = st.selectbox(
            "재구성 방식",
            [
                "원래 수열 g_n",
                "스칼라배 k·g_n",
                "두 등비수열의 곱 g_n · h_n",
                "두 등비수열의 나눗셈 g_n / h_n",
            ],
            key="rec_geo_operation",
        )
    with row2[1]:
        h1 = float(st.number_input("둘째 수열의 첫째항 h1", key="rec_geo_h1", step=1.0))
    with row2[2]:
        s = float(st.number_input("둘째 수열의 공비 s", key="rec_geo_s", step=0.1))

    st.latex(r"g_n = g_1 \cdot r^{n-1}")
    st.latex(r"h_n = h_1 \cdot s^{n-1}")

    button_cols = st.columns([1, 1, 3])
    with button_cols[0]:
        if st.button("그래프 그리기", key="rec_geo_draw"):
            st.session_state["rec_geo_drawn"] = True
    with button_cols[1]:
        if st.button("애니메이션 다시 보기", key="rec_geo_replay"):
            st.session_state["rec_geo_drawn"] = True
            st.session_state["rec_geo_nonce"] += 1

    result = reconstruct_geometric(g1, r, count, operation, h1, s, k)
    if not result["valid"]:
        st.error(result["message"])
        fig = build_message_figure("등비수열 재구성 그래프", "입력값을 조정한 뒤 다시 그래프를 그려 보세요.")
        render_plotly_animation(fig, "rec_geo_invalid", st.session_state["rec_geo_nonce"])
        return

    st.latex(rf"v_n = {result['sequence_latex']}")
    st.latex(rf"y = {result['function_latex']}")

    if not validate_finite_values(result["values"]):
        st.warning("재구성한 값의 크기가 너무 커서 그래프를 안정적으로 표현하기 어렵습니다. 공비나 항의 개수를 조금 줄여 보세요.")
        fig = build_message_figure("등비수열 재구성 그래프", "입력값을 조정하면 재구성 결과를 더 분명하게 볼 수 있습니다.")
        render_plotly_animation(fig, "rec_geo_message", st.session_state["rec_geo_nonce"])
        return

    if st.session_state["rec_geo_drawn"]:
        curve_x = np.linspace(1, max(count, 2), 240)
        with np.errstate(over="ignore", invalid="ignore"):
            curve_y = result["new_first"] * np.power(result["new_ratio"], curve_x - 1)
        if not validate_finite_values(curve_y):
            st.warning("연속 그래프 값이 너무 커서 표시가 어렵습니다. 항의 개수나 공비를 조금 줄여 보세요.")
            fig = build_message_figure("등비수열 재구성 그래프", "입력값을 조정하면 지수적 규칙을 더 선명하게 볼 수 있습니다.")
            render_plotly_animation(fig, "rec_geo_curve_message", st.session_state["rec_geo_nonce"])
        else:
            fig = build_animated_plot(
                result["indices"],
                result["values"],
                curve_x,
                curve_y,
                "재구성한 등비수열과 대응하는 지수함수",
                "재구성한 수열의 점",
                "대응하는 지수함수",
            )
            render_plotly_animation(fig, "rec_geo_chart", st.session_state["rec_geo_nonce"])
    else:
        st.info("재구성 방식을 고른 뒤 `그래프 그리기`를 눌러 식과 그래프를 함께 확인해 보세요.")

    preview_count = min(8, count)
    st.dataframe(
        make_term_dataframe(result["indices"][:preview_count], result["values"][:preview_count], "v_n"),
        use_container_width=True,
        hide_index=True,
    )

    summary_lines = [
        f"새 수열의 일반항: v_n = {result['sequence_expr']}",
        f"처음 몇 개 항: {', '.join(format_number(v) for v in result['values'][:preview_count])}",
        f"첫째항과 공비: ({format_number(result['new_first'])}, {format_number(result['new_ratio'])})",
        result["explanation"],
        "재구성한 점들도 다시 하나의 지수함수적 패턴 위에 놓이는지 살펴보세요.",
    ]
    if result["ratio_note"]:
        summary_lines.append(result["ratio_note"])
    render_summary_card("재구성 결과", summary_lines)


def render_learning_summary_tab() -> None:
    """학습 정리 탭을 렌더링한다."""
    cmp_a1 = float(st.session_state["cmp_arith_a1"])
    cmp_d = float(st.session_state["cmp_arith_d"])
    cmp_g1 = float(st.session_state["cmp_geo_g1"])
    cmp_r = float(st.session_state["cmp_geo_r"])

    rec_arith = reconstruct_arithmetic(
        float(st.session_state["rec_arith_a1"]),
        float(st.session_state["rec_arith_d"]),
        int(st.session_state["rec_arith_n"]),
        str(st.session_state["rec_arith_operation"]),
        float(st.session_state["rec_arith_b1"]),
        float(st.session_state["rec_arith_db"]),
        float(st.session_state["rec_arith_k"]),
    )
    rec_geo = reconstruct_geometric(
        float(st.session_state["rec_geo_g1"]),
        float(st.session_state["rec_geo_r"]),
        int(st.session_state["rec_geo_n"]),
        str(st.session_state["rec_geo_operation"]),
        float(st.session_state["rec_geo_h1"]),
        float(st.session_state["rec_geo_s"]),
        float(st.session_state["rec_geo_k"]),
    )

    render_summary_card(
        "핵심 정리",
        [
            "등차수열은 자연수에서 정의된 일차적 규칙이므로 점들이 대응하는 일차함수 위에 놓입니다.",
            "등비수열은 자연수에서 정의된 지수적 규칙이므로 점들이 대응하는 지수함수적 패턴을 따릅니다.",
            "수열은 이산적 점, 함수는 연속 그래프라는 차이가 있지만 규칙의 구조를 통해 서로 연결해서 이해할 수 있습니다.",
            "재구성한 결과도 첫째항과 공차·공비를 다시 읽어 보면 같은 유형의 규칙인지 판단할 수 있습니다.",
        ],
    )

    left_col, right_col = st.columns(2, gap="large")
    with left_col:
        render_summary_card(
            "현재 등차수열 요약",
            [
                f"비교 탐구 입력: a1={format_number(cmp_a1)}, d={format_number(cmp_d)}",
                f"일반항: a_n = {arithmetic_expr_text(cmp_a1, cmp_d)}",
                f"재구성 결과: u_n = {rec_arith['sequence_expr']}",
                "공차가 일정하면 직선적 변화로 해석할 수 있습니다.",
            ],
        )
    with right_col:
        geo_lines = [
            f"비교 탐구 입력: g1={format_number(cmp_g1)}, r={format_number(cmp_r)}",
            "등비수열은 공비가 양수일 때 지수함수와 자연스럽게 연결됩니다.",
        ]
        if cmp_r > 0:
            geo_lines.append(f"일반항: g_n = {geometric_expr_text(cmp_g1, cmp_r)}")
        else:
            geo_lines.append("현재 비교 탐구의 공비가 0 이하이므로 지수함수 연결은 잠시 보류됩니다.")
        if rec_geo["valid"]:
            geo_lines.append(f"재구성 결과: v_n = {rec_geo['sequence_expr']}")
        else:
            geo_lines.append("재구성 입력을 조정하면 등비수열의 재구성 결과를 다시 확인할 수 있습니다.")
        render_summary_card("현재 등비수열 요약", geo_lines)

    st.markdown("### 교사용 발문")
    prompts = [
        "등차수열의 점들이 왜 하나의 직선 위에 놓인다고 말할 수 있을까요?",
        "수열은 점이고 함수는 연속 그래프인데, 두 대상을 연결해 이해하는 것이 왜 도움이 될까요?",
        "두 등차수열의 합에서 공차가 왜 d+db가 되는지 n번째 항 식으로 설명해 볼까요?",
        "두 등비수열의 곱이나 나눗셈에서 공비가 왜 rs, r/s가 되는지 식과 그래프를 함께 보며 말해 볼까요?",
        "공비가 1인 경우와 공차가 0인 경우는 어떤 점에서 비슷하고 어떤 점에서 다를까요?",
    ]
    for prompt in prompts:
        st.markdown(f"<div class='teacher-prompt'>{prompt}</div>", unsafe_allow_html=True)


def main() -> None:
    """앱 전체를 렌더링한다."""
    initialize_session_state()
    inject_css()
    render_header()

    tabs = st.tabs(["비교 탐구", "재구성 실험", "학습 정리"])

    with tabs[0]:
        compare_tabs = st.tabs(["등차수열 ↔ 일차함수", "등비수열 ↔ 지수함수"])
        with compare_tabs[0]:
            render_arithmetic_compare_section()
        with compare_tabs[1]:
            render_geometric_compare_section()

    with tabs[1]:
        reconstruction_tabs = st.tabs(["등차수열 재구성", "등비수열 재구성"])
        with reconstruction_tabs[0]:
            render_arithmetic_reconstruction_section()
        with reconstruction_tabs[1]:
            render_geometric_reconstruction_section()

    with tabs[2]:
        render_learning_summary_tab()


if __name__ == "__main__":
    main()
