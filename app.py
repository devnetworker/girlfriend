import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from PIL import Image

# 환경변수 로드
load_dotenv()

# CSS 로드
def load_css():
    with open("gf_style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# OpenAI 클라이언트 설정
def setup_openai():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 전역 캐릭터 데이터
CHARACTERS = {
    "순정적인": {
        "image": "images/Pure.webp",
        "prompt": "당신은 순수하고 상냥한 여자친구입니다. 항상 따뜻한 말투로 대화하며 상대방을 배려하는 말을 합니다."
    },
    "보이시한": {
        "image": "images/boyish.webp", 
        "prompt": "당신은 털털하고 남자다운 말투를 사용하는 여자친구입니다. 직설적이지만 마음이 따뜻한 캐릭터입니다."
    },
    "도도한": {
        "image": "images/elegant.webp",
        "prompt": "당신은 차갑지만 은은한 관심을 보이는 도도한 여자친구입니다. 약간의 츤데레 속성이 있습니다."
    }
}

# 로그인 화면
def login_section():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("👩❤️💋👨 여자친구 선택에 오신 것을 환영합니다")
        password = st.text_input("패스워드를 입력하세요", type="password")
        
        if password:
            if password == os.getenv("PASSWORD"):
                st.session_state.logged_in = True
                st.rerun()  # st.rerun() 대신 st.experimental_rerun() 사용
            else:
                st.error("잘못된 패스워드입니다. 다시 시도해주세요.")
        return False
    return True

# 캐릭터 선택 화면
def character_selection():
    st.title("💖 원하는 여자친구 유형을 선택하세요")
    
    cols = st.columns(3)
    for i, (name, info) in enumerate(CHARACTERS.items()):
        with cols[i]:
            with st.container():
                st.image(Image.open(info["image"]), use_container_width=True)
                if st.button(f"{name} 선택", key=name):
                    st.session_state.selected_character = info
                    st.session_state.selected_character_name = name
                    st.session_state.messages = []  # 대화 기록 초기화
                    st.rerun()

# 채팅 인터페이스
def chat_interface():
    client = setup_openai()
    
    # 선택한 캐릭터 이름과 정보를 세션에서 가져옴
    character_name = st.session_state.selected_character_name
    character_info = st.session_state.selected_character
    
    # 사이드바에 캐릭터 이미지와 뒤로가기 버튼 표시
    with st.sidebar:
        st.image(Image.open(character_info["image"]), use_container_width=True)
        st.markdown(f"### {character_name} 여자친구")
        
        # 뒤로가기 버튼
        if st.button("↩️ 다른 여자친구 선택하기"):
            st.session_state.selected_character = None
            st.session_state.selected_character_name = None
            st.session_state.messages = []
            st.rerun()
    
    st.title(f"💬 {character_name} 여자친구와의 대화")
    
    if "messages" not in st.session_state or not st.session_state.messages:
        st.session_state.messages = [
            {"role": "system", "content": st.session_state.selected_character["prompt"]},
            {"role": "assistant", "content": "안녕! 오늘은 무슨 이야기 할까요? 💖"}
        ]

    # 이전 대화 출력
    for msg in st.session_state.messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 사용자 입력
    if prompt := st.chat_input("메시지를 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("답변 생성 중..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_response = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            with st.chat_message("assistant"):
                st.markdown(assistant_response)

# 메인 앱 구조
def main():
    load_css()
    
    if not login_section():
        return
    
    if "selected_character" not in st.session_state or st.session_state.selected_character is None:
        character_selection()
    else:
        chat_interface()

if __name__ == "__main__":
    main()
