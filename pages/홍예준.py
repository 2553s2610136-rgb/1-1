import streamlit as st
import random

st.set_page_config(
    page_title="시험기간의 나",
    page_icon="📚",
    layout="centered"
)

st.title("📚 시험기간의 나")
st.caption("책상에는 앉아 있는데 공부는 안 되는 현실")

# 세션 상태 초기화
if "study_time" not in st.session_state:
    st.session_state.study_time = 0

# 현재 상태 선택
status = st.selectbox(
    "지금 나는 무엇을 하고 있나요?",
    [
        "공부 중",
        "휴대폰 보는 중",
        "유튜브 보는 중",
        "멍 때리는 중",
        "간식 먹는 중"
    ]
)

st.write(f"현재 상태: **{status}**")

# 집중도
focus = st.slider(
    "현재 집중도 (%)",
    min_value=0,
    max_value=100,
    value=50
)

st.progress(focus)

# 집중도 메시지
if focus >= 80:
    st.success("오늘은 꽤 집중하고 있네요! 👍")
elif focus >= 50:
    st.info("나쁘지 않지만 조금만 더 힘내세요!")
else:
    st.warning("집중력이 위험합니다 🚨")

# 공부 목표
goal = st.text_input(
    "오늘의 공부 목표를 적어보세요",
    placeholder="예) 수학 문제집 20쪽 풀기"
)

if goal:
    st.write("🎯 목표:", goal)

st.divider()

# 공부 시간 추가
if st.button("📖 공부 10분 추가"):
    st.session_state.study_time += 10
    st.success("10분 공부 완료!")

st.metric(
    "오늘 누적 공부 시간",
    f"{st.session_state.study_time}분"
)

st.divider()

# 현실 체크
messages = [
    "시험은 다가오는데 휴대폰은 왜 이렇게 재밌을까요?",
    "5분만 쉰다는 말은 보통 30분이 됩니다.",
    "미래의 내가 현재의 나를 보고 있습니다.",
    "한 문제라도 풀면 오늘의 승리입니다.",
    "공부 시작이 가장 어렵습니다."
]

if st.button("😵 현실 체크"):
    st.info(random.choice(messages))

st.divider()

st.subheader("📊 오늘의 상태 요약")

if focus >= 70 and status == "공부 중":
    st.success("시험기간 모범생 모드")
elif status != "공부 중":
    st.warning("공부보다 다른 것에 관심이 가고 있습니다.")
else:
    st.info("조금만 더 집중하면 좋은 결과가 있을 거예요!")

st.caption("Made with Streamlit")
1
