1
import streamlit as st

st.set_page_config(
    page_title="시험기간의 나",
    page_icon="📚",
    layout="centered"
)

# -----------------------------
# 안전한 점수 계산 함수
# -----------------------------
def calculate_score(sleep_hours, motivation, phone_hours, exam_days):
    score = 50

    # 수면
    if sleep_hours >= 7:
        score += 20
    elif sleep_hours >= 5:
        score += 10
    else:
        score -= 10

    # 의욕
    score += motivation * 4

    # 휴대폰 사용
    if phone_hours <= 2:
        score += 15
    elif phone_hours <= 4:
        score += 5
    else:
        score -= 15

    # 시험일
    if exam_days <= 3:
        score += 10
    elif exam_days <= 7:
        score += 5

    return max(0, min(100, score))


# -----------------------------
# 추천 전략
# -----------------------------
def get_tips(score, sleep_hours, phone_hours):
    tips = []

    if sleep_hours < 6:
        tips.append("😴 최소 6~7시간 수면을 확보하세요.")

    if phone_hours > 4:
        tips.append("📵 공부 시간에는 휴대폰을 다른 방에 두세요.")

    if score >= 80:
        tips.append("🚀 현재 상태가 매우 좋습니다. 계획대로 유지하세요.")
        tips.append("📝 어려운 과목을 먼저 공부해 보세요.")

    elif score >= 60:
        tips.append("⏰ 25분 공부 + 5분 휴식의 포모도로 기법을 추천합니다.")
        tips.append("📚 하루 공부 목표를 3개만 정해보세요.")

    else:
        tips.append("🎯 공부 시간을 줄이고 집중도를 높이는 것이 우선입니다.")
        tips.append("📋 오늘 꼭 해야 할 1가지만 먼저 완료해 보세요.")

    return tips


# -----------------------------
# 제목
# -----------------------------
st.title("📚 시험기간의 나")
st.subheader("시험기간 집중력 진단 & 공부 전략 추천")

st.markdown("---")

# -----------------------------
# 입력
# -----------------------------
st.header("🧠 현재 상태 입력")

sleep_hours = st.slider(
    "어제 수면 시간(시간)",
    min_value=0,
    max_value=12,
    value=7
)

motivation = st.slider(
    "공부 의욕 (1~10)",
    min_value=1,
    max_value=10,
    value=5
)

phone_hours = st.slider(
    "하루 휴대폰 사용 시간(시간)",
    min_value=0,
    max_value=12,
    value=3
)

exam_days = st.number_input(
    "시험까지 남은 일수",
    min_value=0,
    max_value=365,
    value=7
)

st.markdown("---")

# -----------------------------
# 결과
# -----------------------------
if st.button("📊 집중력 분석하기"):
    try:
        score = calculate_score(
            sleep_hours,
            motivation,
            phone_hours,
            exam_days
        )

        st.success(f"집중력 점수: {score}점 / 100점")

        if score >= 80:
            st.balloons()
            st.info("🔥 집중 상태가 매우 좋습니다!")
        elif score >= 60:
            st.warning("🙂 집중력이 보통 수준입니다.")
        else:
            st.error("⚠️ 집중력이 낮은 상태입니다.")

        st.subheader("💡 맞춤 공부 전략")

        tips = get_tips(score, sleep_hours, phone_hours)

        for tip in tips:
            st.write("•", tip)

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

st.markdown("---")

# -----------------------------
# 체크리스트
# -----------------------------
st.header("✅ 시험기간 집중 체크리스트")

st.checkbox("오늘 공부 계획 작성")
st.checkbox("휴대폰 알림 끄기")
st.checkbox("공부 공간 정리")
st.checkbox("포모도로 1회 이상 실천")
st.checkbox("7시간 이상 수면 계획")

st.markdown("---")

# -----------------------------
# 다짐 작성
# -----------------------------
st.header("✍️ 오늘의 공부 다짐")

goal = st.text_area(
    "오늘 꼭 이루고 싶은 목표를 적어보세요."
)

if goal:
    st.success("오늘의 다짐")
    st.write(goal)

st.markdown("---")
st.caption("📚 시험기간의 나 | 집중력 부스터")
