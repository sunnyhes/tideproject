import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import font_manager as fm

# 한글 폰트 설정
font_path = "/mount/src/final/NanumGothic.ttf"  # 폰트 경로
font_prop = fm.FontProperties(fname=font_path)  # FontProperties 객체 생성
rc('font', family=font_prop.get_name())  # Matplotlib에 폰트 설정
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 데이터 로드
incheon_data = pd.read_csv("인천조위.csv")
mukho_data = pd.read_csv("묵호조위.csv")
jeju_data = pd.read_csv("제주조위.csv")

# 위치 데이터
data = {
    "지역": ["묵호", "인천", "제주"],
    "latitude": [37.5500, 37.4563, 33.4996],
    "longitude": [129.1167, 126.7052, 126.5312]
}

# 데이터프레임 생성
df = pd.DataFrame(data)

# 제목 표시
st.title("갯벌 체험할 지역 선택하기")

# 복수 선택 메뉴
selected_locations = st.multiselect("지도를 표시할 지역을 선택하세요:", df["지역"], default=df["지역"].tolist())

# 선택한 위치의 데이터 필터링
filtered_df = df[df["지역"].isin(selected_locations)]

# 지도 표시 (선택된 위치가 있을 경우에만)
if not filtered_df.empty:
    st.map(filtered_df, zoom=6)
    st.write(f"선택된 지역: {', '.join(selected_locations)}")
else:
    st.write("선택된 지역이 없습니다.")

# Combine data with an additional column indicating region
incheon_data['Region'] = '인천'
mukho_data['Region'] = '묵호'
jeju_data['Region'] = '제주'

# Merge all data into a single DataFrame
all_data = pd.concat([incheon_data, mukho_data, jeju_data])

# Streamlit app configuration
st.title("조위 그래프 생성기")
st.sidebar.title("옵션 선택")
st.sidebar.info("지역을 선택하여 조위 그래프를 생성하세요.")

# User input: Select regions and month
selected_regions = st.sidebar.multiselect("지역 선택", all_data['Region'].unique(), default=all_data['Region'].unique())

# Filter data based on user selection
filtered_data = all_data[all_data['Region'].isin(selected_regions)]

# Plotting the graph
if not filtered_data.empty:
    st.write(f"### {', '.join(selected_regions)} 지역의 9월 조위 그래프")
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for region in selected_regions:
        region_data = filtered_data[filtered_data['Region'] == region]
        
        # Plot the tide data
        times = pd.to_datetime(region_data['Time'])
        tides = region_data['Predicted_Tide']
        ax.plot(times, tides, label=f'{region} 조위')

    # x축 레이블 간격 및 회전 조정
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))  # 최대 10개 레이블 표시
    plt.xticks(rotation=45, fontproperties=font_prop)  # x축 레이블 45도 회전, 폰트 적용

    # Add titles and labels (폰트 강제 적용)
    ax.set_title(f"9월 조위 그래프", fontproperties=font_prop)
    ax.set_xlabel("시간", fontproperties=font_prop)
    ax.set_ylabel("조위 (cm)", fontproperties=font_prop)
    ax.legend(prop=font_prop)
    ax.grid()
    
    st.pyplot(fig)
else:
    st.warning("선택한 지역/기간의 데이터가 없습니다. 다른 조건을 선택해주세요.")

# 퀴즈 섹션
st.subheader("갯벌 체험 지역 선택하기")
answer = st.text_input("갯벌 체험을 가기 좋은 지역을 그래프를 분석해서 작성하세요", "")

if st.button("제출"):
    # 정답 데이터 (여러 정답 가능)
    correct_answers = {"인천", "서해안"}
    user_answer = answer.strip()  # 입력값의 공백 제거

    # 정답 비교
    if user_answer in correct_answers:
        st.success("정답입니다! 잘했어요!")
    else:
        st.error("틀렸습니다. 다시 시도해보세요.")
