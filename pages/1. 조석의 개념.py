import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import platform

# 한글 폰트 설정
font_path = "/mount/src/final/NanumGothic.ttf"  # 폰트 경로
font_prop = fm.FontProperties(fname=font_path)  # FontProperties 객체 생성
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]
with st.sidebar:
    st.caption(f'{ID}님 접속중')

# 실제 조석 데이터 불러오기
data = pd.read_csv("Ideal_Tide_Data.csv")
data['Timestamp'] = pd.to_datetime(data['Timestamp'])  # Timestamp를 datetime 형식으로 변환

st.title('조석의 개념 배우기')

# 1. 조석의 정의
st.header("조석이란?")
st.write(
    """
    조석은 밀물과 썰물로 인해 해수면의 높이가 주기적으로 높아지고 낮아지는 현상을 말합니다.
    """
)

# 2. 조류
st.header("(1)조류")
st.write(
    """
    조석으로 나타나는 주기적인 해수의 흐름 즉, 밀물과 썰물을 의미합니다.
    """
)
st.image("밀물과 썰물.jpg", caption="썰물과 밀물", use_container_width=True)

# 3. 만조와 간조
st.header("(2) 만조와 간조")
st.write(
    """
    만조는 밀물로 해수면의 높이가 가장 높아질 때를 말하고,
    간조는 썰물로 해수면의 높이가 가장 낮아질 때를 말합니다.
    만조와 간조는 하루에 약 두 번씩 일어납니다.
    """
)

try:
    tide_data = pd.read_csv("Ideal_Tide_Data.csv")  # 파일 경로를 확인해주세요
    tide_data["Timestamp"] = pd.to_datetime(tide_data["Timestamp"])  # 시간 데이터 변환
except FileNotFoundError:
    st.error("데이터 파일이 존재하지 않습니다. 파일 경로를 확인해주세요.")
    st.stop()

# 만조와 간조 식별
tide_data['Maxima'] = (tide_data['Predicted_Tide'] > tide_data['Predicted_Tide'].shift(1)) & \
                      (tide_data['Predicted_Tide'] > tide_data['Predicted_Tide'].shift(-1))
tide_data['Minima'] = (tide_data['Predicted_Tide'] < tide_data['Predicted_Tide'].shift(1)) & \
                      (tide_data['Predicted_Tide'] < tide_data['Predicted_Tide'].shift(-1))

# 만조와 간조 데이터 추출
max_times = tide_data.loc[tide_data['Maxima'], 'Timestamp']
max_tides = tide_data.loc[tide_data['Maxima'], 'Predicted_Tide']
min_times = tide_data.loc[tide_data['Minima'], 'Timestamp']
min_tides = tide_data.loc[tide_data['Minima'], 'Predicted_Tide']

# Streamlit 제목
st.title("조석의 주기 그래프")

# 그래프 그리기
fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(tide_data['Timestamp'], tide_data['Predicted_Tide'], label="조위 변화", color="orange")
ax.scatter(max_times, max_tides, color="red", label="만조")
ax.scatter(min_times, min_tides, color="blue", label="간조")

# 만조와 간조 텍스트 추가
for x, y in zip(max_times, max_tides):
    ax.text(x, y, f"{x.strftime('%H:%M')}", color="red", fontsize=10, ha="center", va="bottom", fontproperties=font_prop)
for x, y in zip(min_times, min_tides):
    ax.text(x, y, f"{x.strftime('%H:%M')}", color="blue", fontsize=10, ha="center", va="top", fontproperties=font_prop)

# 그래프 설정
ax.set_xlabel("시간", fontproperties=font_prop)
ax.set_ylabel("조위 (단위: mm)", fontproperties=font_prop)
ax.set_title("조석의 주기", fontproperties=font_prop)
plt.xticks(rotation=45, fontproperties=font_prop)
ax.legend(prop=font_prop)
ax.grid(True)

# Streamlit에 그래프 출력
st.pyplot(fig)

# 4. 조차
st.header("(3) 조차")
tidal_range = max_tides.values[0] - min_tides.values[0]
st.write(
    f"""
    조차는 만조와 간조 때의 해수면 높이 차이를 의미합니다.
    위 데이터의 조차는 {tidal_range:.2f} mm입니다.
    """
)

# 5. 사리와 조금
st.header("(4) 사리와 조금")
st.write(
    f"""
    한 달 중 조차가 가장 크게 나타나는 시기를 사리, 조차가 가장 작게 나타나는 시기를 조금이라고 한다. 사리와 조금은 한 달에 약 두 번씩 일어난다.
    """
)
st.image("사리와 조금 그래프 이상적 데이터.png", caption="사리와 조금 그래프", use_container_width=True)

tide_data = pd.read_csv("인천조위.csv")
tide_data["Time"] = pd.to_datetime(tide_data["Time"])  # 시간 데이터 변환

# Streamlit 제목
st.title("실제 데이터 그래프")

# 특정 날짜에 텍스트 추가하기 위해 데이터 필터링
annotations = {
    "2024-09-05": "A",
    "2024-09-13": "B",
    "2024-09-20": "C",
    "2024-09-27": "D"
}

# 그래프 그리기
fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(tide_data["Time"], tide_data["Predicted_Tide"], label="조위 변화", color="orange")

# 텍스트 추가
for date, label in annotations.items():
    specific_data = tide_data[tide_data["Time"].dt.strftime("%Y-%m-%d") == date]
    if not specific_data.empty:
        x = specific_data["Time"].iloc[0]
        y = tide_data["Predicted_Tide"].max() + 20
        ax.text(x, y, label, color="blue", fontsize=18, fontweight="bold", ha="center", fontproperties=font_prop)

# x축 텍스트 회전
ax.set_xlabel("시간", fontproperties=font_prop)
ax.set_ylabel("조위 (단위: mm)", fontproperties=font_prop)
ax.set_title("실제 조위 변화 그래프", fontproperties=font_prop)
plt.xticks(rotation=45, fontproperties=font_prop)
ax.legend(prop=font_prop)
ax.grid(True)

# Streamlit에 그래프 출력
st.pyplot(fig)

# 퀴즈 섹션
st.subheader("Quiz: 실제 데이터 그래프를 보고, 사리와 조금의 위치를 고르세요")
sari_answer = st.text_input("사리 위치 (답이 여러개일 경우 쉼표를 써서 구분하세요.)", "")
jogeum_answer = st.text_input("조금 위치 (답이 여러개일 경우 쉼표를 써서 구분하세요.)", "")

if st.button("제출"):
    correct_sari = {"A", "C"}
    correct_jogeum = {"B", "D"}
    user_sari = set(map(str.strip, sari_answer.upper().split(',')))
    user_jogeum = set(map(str.strip, jogeum_answer.upper().split(',')))

    # 정답 비교
    sari_correct = user_sari == correct_sari
    jogeum_correct = user_jogeum == correct_jogeum

    if sari_correct and jogeum_correct:
        st.success("정답입니다! 잘했어요!")
    else:
        st.error("틀렸습니다. 다시 시도해보세요.")
        if not sari_correct:
            st.info(f"사리 정답: {', '.join(correct_sari)}")
        if not jogeum_correct:
            st.info(f"조금 정답: {', '.join(correct_jogeum)}")