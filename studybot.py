import streamlit as st
from pymongo import MongoClient

# MongoDB 연결
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["medical_db"]
collection = db["labeled_data"]

# 키워드 추출 함수 (단순 문자열 분리)
def extract_keywords(text):
    words = text.split()
    keywords = [word for word in words if len(word) > 1 and word not in ["환자", "검사", "증상", "및", "또는", "있습니다"]]
    return keywords

# Streamlit UI
st.title("의학 지식 탐구 챗봇 (Medical Knowledge Explorer Chatbot)")
st.write("키워드를 입력하시면 관련 질문과 정답을 3개 보여드립니다! (예: 기침, 칼슘 보충제) 💊")

# 사용자 입력
keyword_input = st.text_input("키워드 입력:", key="keyword_input")

# 검색 및 결과 출력
if keyword_input:
    # 입력에서 키워드 추출
    keywords = extract_keywords(keyword_input)
    if not keywords:
        st.write("유의미한 키워드를 추출하지 못했습니다. 다른 키워드를 입력해주세요.")
    else:
        # MongoDB에서 키워드와 매칭되는 데이터 검색
        results = collection.find({"keywords": {"$in": keywords}}).limit(3)
        results = list(results)
        
        if results:
            st.write("### 관련 질문과 정답")
            for i, result in enumerate(results, 1):
                st.write(f"**{i}. 진료과**: {result['department']}")
                st.write(f"**질문**: {result['question']}")
                st.write(f"**정답**: {result['answer']}")
                st.write("---")
        else:
            st.write("관련 질문을 찾을 수 없습니다. 다른 키워드를 입력해보세요.")