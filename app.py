import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 비밀번호 확인
if "authenticated" not in st.session_state:
    password = st.text_input("비밀번호를 입력하세요", type="password", key="pw")
    if password != "test1234!!":
        st.error("잘못된 비밀번호입니다")
        st.stop()
    st.session_state.authenticated = True
    st.rerun()

st.title("AI 여자친구 채팅")

with st.sidebar:
    # st.header("설정")
    # api_key = st.text_input("OpenAI API 키", 
    #                       type="password", 
    #                       value=os.getenv("OPENAI_API_KEY", ""),
    #                       key="api_key")
    api_key = os.getenv("OPENAI_API_KEY", "")
    system_prompt = st.text_area(
        "시스템 프롬프트",
        value=os.getenv("SYSTEM_PROMPT", "사랑스러운 20대 여자친구처럼 대답해줘. 정치, 경제 등 연애와 관련 없는 주제의 질문에는 '저는 그런 건 잘 모르는 여자친구예요~ 우리 연애 이야기만 해요'라고 답변해줘"),
        key="system_prompt",
        max_chars=1000
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("메시지를 입력하세요")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("답변 생성 중..."):
        client = OpenAI(api_key=api_key)
        
        messages = [{"role": "system", "content": system_prompt}]
        messages += [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})