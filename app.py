import streamlit as st
import pandas as pd
import time
import streamlit as st

# 초기화 상태 확인 및 설정
if 'key' not in st.session_state:
    st.session_state['key'] = '초기값'

# 이후에 상태를 활용
st.write(f"현재 상태: {st.session_state['key']}")


st.title("해수의 순환- part 4. 조석 ")
st.image('조석.png')
data = pd.read_csv("members.csv")
data["PW"] = data["PW"].astype(str)

with st.form("login_form"):
    ID = st.text_input("ID", placeholder="아이디를 입력하세요")
    PW = st.text_input("Password", type="password", placeholder="비밀번호를 입력하세요")
    submit_button = st.form_submit_button("로그인")

if submit_button:
    if not ID or not PW:
        st.warning("ID와 비밀번호를 모두 입력해주세요.")
    else:
        # 사용자 확인
        user = data[(data["ID"] == ID) & (data["PW"] == str(PW))]
        
        if not user.empty:
            st.success(f"{ID}님 환영합니다!")
            st.session_state["ID"]=ID
            
            progress_text = "로그인 중입니다."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            my_bar.empty()
            st.switch_page("pages/1. 조석의 개념.py")
            
            
        else:
            st.error("아이디 또는 비밀번호가 일치하지 않습니다.")