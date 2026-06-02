import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="배드민턴 AI 챗봇",
    page_icon="🏸"
)

st.title("🏸 배드민턴 AI 챗봇")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 초기화 오류: {e}")
    st.stop()

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 배드민턴에 관한 질문을 해보세요. 🏸"
        }
    ]

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
prompt = st.chat_input("배드민턴 질문을 입력하세요")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini에 전달할 대화 구성
    history_text = ""

    for msg in st.session_state.messages:
        role = "사용자" if msg["role"] == "user" else "AI"
        history_text += f"{role}: {msg['content']}\n"

    full_prompt = f"""
당신은 배드민턴 전문 코치입니다.

다음 대화 기록을 참고하여 답변하세요.

{history_text}

AI:
"""

    try:
        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=full_prompt
                )

                answer = response.text

                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    except Exception as e:
        error_msg = f"오류가 발생했습니다: {e}"

        with st.chat_message("assistant"):
            st.error(error_msg)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_msg
            }
        )
