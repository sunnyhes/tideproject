import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image

# 한글 폰트 설정
font_path = "/mount/src/tideproject/NanumGothic.ttf"  # NanumGothic 폰트 경로
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 업로드된 이미지를 딕셔너리로 매핑
moon_images = {
    "그믐달": "pages/그믐달.jpg",
    "초승달": "pages/초승달.jpg",
    "상현달": "pages/상현달.jpg",
    "망": "pages/망.jpg",
    "하현달": "pages/하현달.jpg",
    "삭": "pages/삭.png"
}


# 양력과 음력 날짜 매핑
gregorian_to_lunar = {
    "2024-09-01": "7월 29일",
    "2024-09-02": "7월 30일",
    "2024-09-03": "8월 1일",
    "2024-09-04": "8월 2일",
    "2024-09-05": "8월 3일",
    "2024-09-06": "8월 4일",
    "2024-09-07": "8월 5일",
    "2024-09-08": "8월 6일",
    "2024-09-09": "8월 7일",
    "2024-09-10": "8월 8일",
    "2024-09-11": "8월 9일",
    "2024-09-12": "8월 10일",
    "2024-09-13": "8월 11일",
    "2024-09-14": "8월 12일",
    "2024-09-15": "8월 13일",
    "2024-09-16": "8월 14일",
    "2024-09-17": "8월 15일",
    "2024-09-18": "8월 16일",
    "2024-09-19": "8월 17일",
    "2024-09-20": "8월 18일",
    "2024-09-21": "8월 19일",
    "2024-09-22": "8월 20일",
    "2024-09-23": "8월 21일",
    "2024-09-24": "8월 22일",
    "2024-09-25": "8월 23일",
    "2024-09-26": "8월 24일",
    "2024-09-27": "8월 25일",
    "2024-09-28": "8월 26일",
    "2024-09-29": "8월 27일",
    "2024-09-30": "8월 28일"
}

# 달의 위상 매핑
phase_mapping = {
    "2024-09-01": "그믐달",
    "2024-09-02": "그믐달",
    "2024-09-03": "삭",
    "2024-09-04": "초승달",
    "2024-09-05": "초승달",
    "2024-09-06": "초승달",
    "2024-09-07": "초승달",
    "2024-09-08": "초승달",
    "2024-09-09": "상현달",
    "2024-09-10": "상현달",
    "2024-09-11": "상현달",
    "2024-09-12": "상현달",
    "2024-09-13": "상현달",
    "2024-09-14": "상현달",
    "2024-09-15": "상현달",
    "2024-09-16": "상현달",
    "2024-09-17": "망",
    "2024-09-18": "망",
    "2024-09-19": "망",
    "2024-09-20": "망",
    "2024-09-21": "망",
    "2024-09-22": "망",
    "2024-09-23": "망",
    "2024-09-24": "하현달",
    "2024-09-25": "하현달",
    "2024-09-26": "하현달",
    "2024-09-27": "하현달",
    "2024-09-28": "하현달",
    "2024-09-29": "그믐달",
    "2024-09-30": "그믐달"
}


# 날짜 범위 생성
dates = pd.date_range(start="2024-09-01", end="2024-09-30")

# Streamlit 제목
st.title("24년 9월 달의 위상과 조위 그래프")

# 조위 데이터 불러오기
file_path = '인천조위10분.csv'
tidal_data = pd.read_csv(file_path)
tidal_data['Timestamp'] = pd.to_datetime(tidal_data['Timestamp'])
tidal_data['Date'] = tidal_data['Timestamp'].dt.date

# **달의 위상**
selected_date = st.slider(
    "날짜를 선택하세요:",
    min_value=dates.min().to_pydatetime(),
    max_value=dates.max().to_pydatetime(),
    value=dates.min().to_pydatetime(),
    format="YYYY-MM-DD"
)

selected_date_str = selected_date.strftime("%Y-%m-%d")
lunar_date = gregorian_to_lunar[selected_date_str]
phase_type = phase_mapping[selected_date_str]

st.subheader(f"선택한 날짜: {selected_date.strftime('%Y-%m-%d')}")
st.write(f"📅 **음력 날짜:** {lunar_date}")
st.write(f"🔄 **달의 형태:** {phase_type}")

if phase_type in moon_images:
    image_path = moon_images[phase_type]
    try:
        image = Image.open(image_path)
        st.image(image, caption=f"{phase_type}", width=300)
    except Exception as e:
        st.error(f"이미지를 로드하는 중 오류 발생: {e}")
else:
    st.error("해당 날짜에 대한 이미지가 없습니다.")

# **달의 위상 선택에 따른 조위 그래프**
selected_phases = st.sidebar.multiselect(
    "달의 위상을 선택하세요 (다중 가능):",
    ["그믐달", "초승달", "상현달", "망", "하현달", "삭"],
    default=["삭"]
)
selected_dates = [
    date for date, phase in phase_mapping.items() if phase in selected_phases
]
filtered_tidal_data = tidal_data[tidal_data['Date'].isin(pd.to_datetime(selected_dates).date)]

if not filtered_tidal_data.empty:
    st.subheader(f"선택한 위상들의 조위 그래프")
    fig, ax = plt.subplots(figsize=(10, 5))
    for date in filtered_tidal_data['Date'].unique():
        date_data = filtered_tidal_data[filtered_tidal_data['Date'] == date]
        time_as_hours = (date_data['Timestamp'] - date_data['Timestamp'].dt.normalize()).dt.total_seconds() / 3600
        ax.plot(time_as_hours, date_data['Predicted_Tide'], label=f"{date}")
    ax.set_xlabel('시간 (시)', fontproperties=font_prop)
    ax.set_ylabel('조위 (cm)', fontproperties=font_prop)
    ax.set_ylim(0, 1000)
    ax.legend(prop=font_prop)
    ax.set_title("선택한 위상의 조위 그래프", fontproperties=font_prop)
    st.pyplot(fig)
else:
    st.warning("선택한 위상에 대한 조위 데이터가 없습니다.")

st.subheader("갯벌 체험 날짜 선택하기")    
 # 사용자 입력
answer = st.text_input("갯벌 체험을 가기 좋은 날짜를 그래프를 분석해서 작성하세요(2024-09-01과 같은 양식으로 답을 작성하세요.)", "")

# 정답 확인
if st.button("제출"):
    # 정답 데이터 (여러 정답 가능)
    correct_answers = {"2024-09-19"}
    
    # 사용자 입력 처리
    user_answer = answer.strip()  # 입력값의 공백 제거
    
    # 정답 비교
    if user_answer in correct_answers:
        st.success("정답입니다! 잘했어요!")
    else:
        st.error("틀렸습니다. 다시 시도해보세요.")
        
           
# **일별 조위 그래프**
st.subheader("일별 조위 그래프")
selected_date_for_daily_graph = st.selectbox("조위 그래프를 볼 날짜를 선택하세요:", dates.strftime('%Y-%m-%d'))
daily_data = tidal_data[tidal_data['Date'] == pd.to_datetime(selected_date_for_daily_graph).date()]

if not daily_data.empty:
    # 09시부터 16시 사이의 데이터 필터링
    daily_data_filtered = daily_data[
        (daily_data['Timestamp'].dt.hour >= 9) & (daily_data['Timestamp'].dt.hour <= 16)
    ]

    # 간조 계산 (가장 낮은 조위 값 및 시각 찾기)
    if not daily_data_filtered.empty:
        low_tide_idx = daily_data_filtered['Predicted_Tide'].idxmin()
        low_tide_time = daily_data_filtered.loc[low_tide_idx, 'Timestamp']
        low_tide_value = daily_data_filtered.loc[low_tide_idx, 'Predicted_Tide']

        # 간조 시각 출력
        st.write(f"🌊 **간조 시각:** {low_tide_time.strftime('%H:%M:%S')} (조위: {low_tide_value} cm)")

        # 조위 그래프
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(daily_data['Timestamp'], daily_data['Predicted_Tide'], label="조위")
        ax.axvline(low_tide_time, color='red', linestyle='--', label="간조")  # 간조 시각 표시
        ax.set_xlabel('시간', fontproperties=font_prop)
        ax.set_ylabel('조위 (cm)', fontproperties=font_prop)
        ax.set_title(f"{selected_date_for_daily_graph} 조위 그래프", fontproperties=font_prop)
        ax.legend(prop=font_prop)
        st.pyplot(fig)
    else:
        st.warning("09시부터 16시 사이에 데이터가 없습니다.")
else:
    st.warning("선택한 날짜에 대한 조위 데이터가 없습니다.")

st.subheader("갯벌 체험 시간 결정하기")

# 사용자 입력
answer2 = st.text_input("갯벌 체험을 가기 가장 좋은 시간을 작성하세요(16:30과 같은 양식으로 답을 작성하세요.)", "")

# 정답 확인
if st.button("제출", key="quiz_submit"):
    # 정답 데이터 (여러 정답 가능)
    correct_answers2 = {"11:50"}
    
    # 사용자 입력 처리
    user_answer2 = answer2.strip()  # 입력값의 공백 제거
    
    # 정답 비교
    if user_answer2 in correct_answers2:
        st.success("정답입니다! 잘했어요!")
    else:
        st.error("틀렸습니다. 다시 시도해보세요.")
