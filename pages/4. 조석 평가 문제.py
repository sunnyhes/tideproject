import streamlit as st
import time 

# 문제와 정답 정의
questions = [
    {
        "question": "다음 물음에 해당하는 것의 기호를 |보기|에서 골라 쓰시오.",
        "choices": "|  **ㄱ. 조류**   |  **ㄴ. 조석**   |  **ㄷ. 해류**   |  **ㄹ. 간조**   |  **ㅁ. 조차**   |",
        "sub_questions": [
            {"text": "조석에 의한 바닷물의 흐름은 (       )이다.", "answer": "ㄱ"},
            {"text": "만조와 간조 때 해수면의 높이 차이는 (       )이다.", "answer": "ㅁ"},
            {"text": "밀물과 썰물에 따라 해수면의 높이가 주기적으로 오르내리는 현상은 (       )이다.", "answer": "ㄴ"}
        ]
    },
    {
        "question": "다음은 조석 현상에 관한 설명이다. 빈칸에 알맞은 말을 고르시오.",
        "sub_questions": [
            {"text": "해수면의 높이는 하루에 약 ( 한 번 , 두 번 )씩 주기적으로 높아지거나 낮아진다.",
             "options": ["한 번", "두 번"], "answer": "두 번"},
            {"text": "조차가 큰 우리나라 ( 동해안 , 서해안 )에서는 넓은 갯벌이 만들어진다.",
             "options": ["동해안", "서해안"], "answer": "서해안"}
        ]
    },
    {
        "question": "그림은 우리나라 해안의 조석 현상에 관한 실시간 자료를 나타낸 것이다.\n\n"
                    "이에 관한 설명으로 옳은 것만을 |보기|에서 있는 대로 고른 것은?",
        "image": "문제3.png",
        "caption": "우리나라 해안 조석 현상 실시간 자료",
        "choices": """
        <ul style="color: black;">
            <li><b>ㄱ.</b> 해당 지역의 현재 시각은 밀물 때이다.</li>
            <li><b>ㄴ.</b> 하루에 만조와 간조는 약 두 번씩 나타난다.</li>
            <li><b>ㄷ.</b> 18시경에 갯벌 체험을 할 수 있다.</li>
        </ul>
        """,
        "options": ["① ㄱ", "② ㄴ", "③ ㄱ, ㄷ", "④ ㄴ, ㄷ", "⑤ ㄱ, ㄴ, ㄷ"],
        "answer": "② ㄴ"
    },
    {
        "question": "그림은 어느 날 하루 동안 해수면의 높이 변화를 나타낸 것이다.\n\n"
                    "A~D에 관한 설명으로 옳은 것만을 |보기|에서 있는 대로 고른 것은?",
        "image": "문제4.png",
        "caption": "하루 동안 해수면 높이 변화 그래프",
        "choices": """
        <ul style="color: black;">
            <li><b>ㄱ.</b> A는 밀물 때이다.</li>
            <li><b>ㄴ.</b> B는 해수면이 가장 높아진 때인 간조이다.</li>
            <li><b>ㄷ.</b> C는 썰물 때이다.</li>
            <li><b>ㄹ.</b> D는 해수면이 가장 낮아진 때인 만조이다.</li>
        </ul>
        """,
        "options": ["① ㄱ, ㄴ", "② ㄱ, ㄷ", "③ ㄴ, ㄷ", "④ ㄴ, ㄹ", "⑤ ㄷ, ㄹ"],
        "answer": "② ㄱ, ㄷ"
    },
    {
        "question": "그림은 넓게 드러난 갯벌의 모습을 나타낸 것이다.\n\n"
                    "이에 관한 설명으로 옳은 것만을 |보기|에서 있는 대로 고른 것은?",
        "image": "문제5.png",
        "caption": "넓게 드러난 갯벌의 모습",
        "choices": """
        <ul style="color: black;">
            <li><b>ㄱ.</b> 간조일 때의 모습이다.</li>
            <li><b>ㄴ.</b> 보통 하루에 한 번씩만 볼 수 있다.</li>
            <li><b>ㄷ.</b> 조차가 큰 지역에서 잘 볼 수 있다.</li>
        </ul>
        """,
        "options": ["① ㄱ", "② ㄷ", "③ ㄱ, ㄷ", "④ ㄴ, ㄷ", "⑤ ㄱ, ㄴ, ㄷ"],
        "answer": "③ ㄱ, ㄷ"
    }
]

# UI 설정
st.title("조석 개념 형성평가")
user_answers = []

# 각 문제 출력
for i, question in enumerate(questions):
    st.subheader(f"문제 {i + 1}")
    st.write(question["question"])
    
    # 1번 문제 처리
    if i == 0:  # 단답식 문제
        st.markdown(question["choices"])
        for j, sub_q in enumerate(question["sub_questions"]):
            formatted_text = sub_q["text"].replace("(       )", "(      )")  # 공백 조정
            user_answer = st.text_input(formatted_text, key=f"q{i}_{j}")
            user_answers.append({"question": sub_q["text"], "answer": sub_q["answer"], "user_answer": user_answer})

    # 2번 문제 처리
    elif i == 1:  # 선택형 문제
        for j, sub_q in enumerate(question["sub_questions"]):
            user_answer = st.radio(sub_q["text"], options=sub_q["options"], key=f"q{i}_{j}")
            user_answers.append({"question": sub_q["text"], "answer": sub_q["answer"], "user_answer": user_answer})

    # 3, 4, 5번 문제 처리
    elif i >= 2:
        # 이미지 출력
        if "image" in question:
            st.image(question["image"], caption=question["caption"], use_container_width=True)
        
        # 보기 출력
        st.markdown(f"""
        <div style="border: 1px solid #000; padding: 10px; border-radius: 5px; background-color: #f9f9f9; color: black;">
            <strong>보기</strong>
            {question["choices"]}
        </div>
        """, unsafe_allow_html=True)

        # 답 선택
        user_answer = st.radio("답을 선택하세요:", options=question["options"], key=f"q{i}")
        user_answers.append({"question": question["question"], "answer": question["answer"], "user_answer": user_answer})

# 제출 및 채점
if st.button("제출"):
    st.write("**채점 결과**")
    score = 0
    for ua in user_answers:
        if ua["user_answer"] == ua["answer"]:
            st.write(f"✔️ {ua['question']} - 정답입니다!")
            score += 1
        else:
            st.write(f"❌ {ua['question']} - 오답입니다. 정답: {ua['answer']}")
    st.write(f"총 점수: {score} / {len(user_answers)}")

            
            
       # 진행 표시
    progress_text = "5초 후에 다음 페이지로 이동합니다."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
         time.sleep(0.05)  
         my_bar.progress(percent_complete + 1, text=progress_text)
    
    # 페이지 이동
    st.write("페이지로 이동 중...")
    st.session_state["quiz_completed"] = True  
    st.switch_page("pages/5. 조석 과제 제출.py")  
            