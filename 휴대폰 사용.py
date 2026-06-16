import streamlit as st

st.set_page_config(
    page_title="시험기간 휴대폰 사용 관리",
    page_icon="📱",
    layout="centered"
)

st.title("📱 시험기간 휴대폰 사용 관리 도우미")
st.markdown(
    """
시험기간 동안 휴대폰 사용 습관을 점검하고,
공부 시간을 얼마나 확보할 수 있는지 확인해보세요.
"""
)

try:
    st.subheader("📝 현재 상황 입력")

    daily_phone_time = st.slider(
        "하루 평균 휴대폰 사용 시간(시간)",
        min_value=0.0,
        max_value=12.0,
        value=3.0,
        step=0.5
    )

    study_time = st.slider(
        "하루 평균 공부 시간(시간)",
        min_value=0.0,
        max_value=15.0,
        value=4.0,
        step=0.5
    )

    days_left = st.number_input(
        "시험일까지 남은 일수",
        min_value=1,
        max_value=365,
        value=14
    )

    if st.button("결과 확인하기"):

        total_phone_time = daily_phone_time * days_left

        potential_recovery = total_phone_time * 0.5

        score = 100

        score -= daily_phone_time * 8
        score += study_time * 3

        score = max(0, min(100, int(score)))

        st.subheader("📊 분석 결과")

        st.metric(
            "시험 전 예상 휴대폰 사용 시간",
            f"{total_phone_time:.1f}시간"
        )

        st.metric(
            "절반만 줄여도 확보 가능한 공부 시간",
            f"{potential_recovery:.1f}시간"
        )

        st.metric(
            "시험 집중 준비 점수",
            f"{score}점"
        )

        if score >= 80:
            level = "매우 좋음 🟢"
            advice = """
현재 습관을 유지하면 좋습니다.

- 공부 중 알림 끄기
- SNS 확인 시간 정하기
- 취침 전 휴대폰 사용 줄이기
"""
        elif score >= 60:
            level = "보통 🟡"
            advice = """
휴대폰 사용을 조금만 줄여도 큰 효과가 있습니다.

- 공부 시간에는 방해 금지 모드 사용
- 30분 공부 후 5분 휴식
- 짧은 영상 시청 시간 제한
"""
        else:
            level = "주의 🔴"
            advice = """
휴대폰 사용 습관 개선이 필요합니다.

- SNS 앱 사용 시간 제한 설정
- 공부 공간에서 휴대폰 멀리 두기
- 공부 시작 전 비행기 모드 활용
- 하루 목표 공부 시간 정하기
"""

        st.subheader("🎯 집중도 평가")
        st.success(level)

        st.subheader("💡 맞춤 추천")
        st.info(advice)

        st.subheader("📈 예상 변화")

        reduced_phone = daily_phone_time * 0.7
        saved_time = (daily_phone_time - reduced_phone) * days_left

        st.write(
            f"하루 휴대폰 사용을 30%만 줄여도 시험일까지 약 **{saved_time:.1f}시간**을 추가로 확보할 수 있습니다."
        )

except Exception as e:
    st.error("오류가 발생했습니다.")
    st.exception(e)

st.markdown("---")
st.caption("시험기간 집중력 향상을 위한 간단한 자기 점검 도구")
