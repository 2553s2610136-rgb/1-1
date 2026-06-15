import streamlit as st
from datetime import datetime, date, timedelta
import time

st.set_page_config(
    page_title="시험기간 집중 타이머",
    page_icon="📚",
    layout="centered"
)

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "running" not in st.session_state:
    st.session_state.running = False

if "end_time" not in st.session_state:
    st.session_state.end_time = None

if "study_seconds" not in st.session_state:
    st.session_state.study_seconds = 0

if "mode" not in st.session_state:
    st.session_state.mode = "공부"

# -----------------------------
# 제목
# -----------------------------
st.title("📚 시험기간 집중 타이머")
st.caption("시험일까지 남은 기간과 공부 시간을 함께 관리하세요")

st.divider()

# -----------------------------
# 시험일 설정
# -----------------------------
st.subheader("🎯 시험 일정")

exam_date = st.date_input(
    "시험 날짜 선택",
    value=date.today() + timedelta(days=14)
)

days_left = (exam_date - date.today()).days

if days_left > 0:
    st.success(f"시험까지 **D-{days_left}**")
elif days_left == 0:
    st.warning("🔥 시험 당일입니다!")
else:
    st.error(f"시험이 {-days_left}일 지났습니다.")

st.divider()

# -----------------------------
# 공부 목표
# -----------------------------
st.subheader("📈 오늘의 목표")

goal_hours = st.slider(
    "목표 공부 시간 (시간)",
    min_value=1,
    max_value=12,
    value=4
)

goal_seconds = goal_hours * 3600

# -----------------------------
# 포모도로 설정
# -----------------------------
st.subheader("⏰ 집중 타이머")

study_min = st.number_input(
    "공부 시간(분)",
    min_value=1,
    max_value=180,
    value=25
)

break_min = st.number_input(
    "휴식 시간(분)",
    min_value=1,
    max_value=60,
    value=5
)

col1, col2 = st.columns(2)

with col1:
    start_btn = st.button("▶ 시작", use_container_width=True)

with col2:
    stop_btn = st.button("■ 정지", use_container_width=True)

if start_btn:
    st.session_state.running = True

    if st.session_state.mode == "공부":
        duration = study_min * 60
    else:
        duration = break_min * 60

    st.session_state.end_time = time.time() + duration

if stop_btn:
    st.session_state.running = False

# -----------------------------
# 타이머 표시
# -----------------------------
timer_placeholder = st.empty()

if st.session_state.running and st.session_state.end_time:

    remaining = int(st.session_state.end_time - time.time())

    if remaining <= 0:

        st.session_state.running = False

        if st.session_state.mode == "공부":
            st.session_state.study_seconds += study_min * 60
            st.session_state.mode = "휴식"
            st.success("공부 시간 종료! 휴식하세요 😄")
        else:
            st.session_state.mode = "공부"
            st.success("휴식 종료! 다시 집중하세요 🚀")

        st.rerun()

    else:
        mins = remaining // 60
        secs = remaining % 60

        timer_placeholder.markdown(
            f"""
            <h1 style='text-align:center'>
            {mins:02d}:{secs:02d}
            </h1>
            <h3 style='text-align:center'>
            현재 모드 : {st.session_state.mode}
            </h3>
            """,
            unsafe_allow_html=True
        )

        time.sleep(1)
        st.rerun()

else:
    timer_placeholder.markdown(
        f"""
        <h1 style='text-align:center'>
        준비 완료
        </h1>
        <h3 style='text-align:center'>
        현재 모드 : {st.session_state.mode}
        </h3>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# 누적 공부 시간
# -----------------------------
st.divider()

st.subheader("📊 오늘의 진행률")

study_hours = st.session_state.study_seconds / 3600

progress = min(
    st.session_state.study_seconds / goal_seconds,
    1.0
)

st.progress(progress)

st.metric(
    "누적 공부 시간",
    f"{study_hours:.2f}시간"
)

st.metric(
    "목표 달성률",
    f"{progress * 100:.1f}%"
)

# -----------------------------
# 공부 팁
# -----------------------------
st.divider()

tips = [
    "25분 집중 + 5분 휴식은 가장 널리 사용되는 포모도로 방식입니다.",
    "휴식 시간에는 스마트폰보다 스트레칭이 더 효과적입니다.",
    "목표 시간을 작게 나누면 집중력이 오래 유지됩니다.",
    "시험 전날보다 매일 꾸준히 하는 것이 더 중요합니다."
]

st.info(tips[datetime.now().minute % len(tips)])
