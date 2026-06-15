import streamlit as st
from datetime import date, datetime
import pandas as pd

st.set_page_config(
    page_title="시험기간 집중 앱",
    page_icon="📚",
    layout="wide"
)

# ------------------------
# Session State 초기화
# ------------------------
if "study_log" not in st.session_state:
    st.session_state.study_log = []

if "subjects" not in st.session_state:
    st.session_state.subjects = []

# ------------------------
# 제목
# ------------------------
st.title("📚 시험기간 집중 앱")
st.caption("시험까지 남은 기간을 관리하고 집중력을 높여보세요.")

# ------------------------
# 사이드바
# ------------------------
with st.sidebar:
    st.header("⚙️ 시험 설정")

    exam_date = st.date_input(
        "시험 날짜",
        value=date.today()
    )

    days_left = (exam_date - date.today()).days

    if days_left > 0:
        st.success(f"D-{days_left}")
    elif days_left == 0:
        st.warning("시험 당일입니다!")
    else:
        st.error("시험 날짜가 지났습니다.")

# ------------------------
# 탭 구성
# ------------------------
tab1, tab2, tab3 = st.tabs(
    ["🎯 오늘의 목표", "⏱️ 집중 관리", "📊 학습 현황"]
)

# ==================================================
# 탭1
# ==================================================
with tab1:

    st.subheader("오늘의 공부 목표")

    with st.form("goal_form"):

        subject = st.text_input("과목명")

        target_hours = st.number_input(
            "목표 공부 시간(시간)",
            min_value=1,
            max_value=24,
            value=4
        )

        target_progress = st.text_input(
            "목표 진도 (예: 3단원 완료)"
        )

        submitted = st.form_submit_button("목표 저장")

        if submitted:
            if subject.strip():

                st.session_state.subjects.append(
                    {
                        "subject": subject,
                        "target_hours": target_hours,
                        "target_progress": target_progress,
                        "done": False
                    }
                )

                st.success("목표가 저장되었습니다.")

            else:
                st.warning("과목명을 입력해주세요.")

    st.divider()

    if st.session_state.subjects:

        st.subheader("등록된 목표")

        for idx, item in enumerate(st.session_state.subjects):

            col1, col2 = st.columns([4, 1])

            with col1:
                checked = st.checkbox(
                    f"{item['subject']} | {item['target_hours']}시간 | {item['target_progress']}",
                    value=item["done"],
                    key=f"subject_{idx}"
                )

                st.session_state.subjects[idx]["done"] = checked

            with col2:
                if checked:
                    st.success("완료")

# ==================================================
# 탭2
# ==================================================
with tab2:

    st.subheader("집중 세션")

    focus_option = st.selectbox(
        "집중 시간 선택",
        ["25분", "50분", "직접 입력"]
    )

    if focus_option == "25분":
        focus_time = 25

    elif focus_option == "50분":
        focus_time = 50

    else:
        focus_time = st.number_input(
            "분 입력",
            min_value=1,
            max_value=300,
            value=30
        )

    st.info(
        f"추천 집중 시간: {focus_time}분"
    )

    if st.button("공부 완료 기록"):

        st.session_state.study_log.append(
            {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "minutes": focus_time
            }
        )

        st.success(
            f"{focus_time}분 공부가 기록되었습니다."
        )

# ==================================================
# 탭3
# ==================================================
with tab3:

    st.subheader("학습 현황")

    total_minutes = sum(
        item["minutes"]
        for item in st.session_state.study_log
    )

    total_hours = round(total_minutes / 60, 1)

    completed = sum(
        1 for item in st.session_state.subjects
        if item["done"]
    )

    total_subjects = len(st.session_state.subjects)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "총 공부 시간",
        f"{total_hours}시간"
    )

    col2.metric(
        "완료 목표",
        f"{completed}/{total_subjects}"
    )

    readiness = 0

    if total_subjects > 0:
        readiness = int(
            (completed / total_subjects) * 100
        )

    col3.metric(
        "시험 준비도",
        f"{readiness}%"
    )

    st.progress(readiness)

    st.divider()

    if st.session_state.study_log:

        st.subheader("공부 기록")

        df = pd.DataFrame(
            st.session_state.study_log
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    else:
        st.info("아직 공부 기록이 없습니다.")
