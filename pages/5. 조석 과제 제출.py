from google.oauth2.service_account import Credentials
import streamlit as st
import gspread

# Google Sheets API 인증 범위 설정
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Streamlit Secrets에서 자격 증명 불러오기
credentials_dict = st.secrets["gcp_service_account"]

# Credentials 객체 생성
creds = Credentials.from_service_account_info(credentials_dict, scopes=scope)

# gspread 클라이언트 생성
client = gspread.authorize(creds)

# '답안' 시트 열기 (없으면 생성)
try:
    answer_sheet = client.open("조석 이용 사례 제출").worksheet("답안")
except gspread.exceptions.WorksheetNotFound:
    answer_sheet = client.open("조석 이용 사례 제출").add_worksheet(title="답안", rows="1000", cols="4")

# Streamlit 앱 내용
st.title("조석의 이용 사례 과제 제출")

# 예시 내용 (유지)
st.subheader("조석 이용 사례 과제 예시")

image1_path = "사진1.jpg"
image2_path = "사진2.jpg"

row1_col1, row1_col2, row1_col3 = st.columns([1, 2, 3])
row2_col1, row2_col2, row2_col3 = st.columns([1, 2, 3])

with row1_col1:
    st.markdown("<div style='text-align: center;'><b>활동</b></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>조개 캐기</div>", unsafe_allow_html=True)
with row1_col2:
    st.markdown("<div style='text-align: center;'><b>이미지</b></div>", unsafe_allow_html=True)
    st.image(image1_path, caption="조개 캐기", width=150)
with row1_col3:
    st.markdown("<div style='text-align: center;'><b>설명</b></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>간조 때 넓게 드러난 갯벌에서 조개를 캔다.</div>", unsafe_allow_html=True)

with row2_col1:
    st.markdown("<div style='text-align: center;'>고기잡이</div>", unsafe_allow_html=True)
with row2_col2:
    st.image(image2_path, caption="고기잡이", width=150)
with row2_col3:
    st.markdown("<div style='text-align: center;'>바다에 돌담이나 그물을 세우고 조류를 이용하여 물고기를 잡는다.</div>", unsafe_allow_html=True)

# 학생 제출 폼
st.subheader("학생 제출 폼")
name = st.text_input("이름")  # 이름 입력
activity = st.text_input("활동")  # 활동 입력
description = st.text_area("설명")  # 설명 입력
image_url = st.text_input("이미지 URL")  # 이미지 URL 입력

if st.button("제출"):
    if name and activity and description and image_url:
        # Google Sheets에 제출된 데이터 추가
        answer_sheet.append_row([name, activity, description, image_url])  # 데이터만 저장
        st.success("제출이 완료되었습니다!")
    else:
        st.error("모든 필드를 입력해주세요.")

