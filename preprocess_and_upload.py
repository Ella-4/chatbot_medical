from pymongo import MongoClient
import json
import os

# MongoDB 연결
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["medical_db"]
collection = db["labeled_data"]

# 기존 데이터 삭제 (새로 업로드 위해)
collection.delete_many({})
print("기존 데이터 삭제 완료")

# 키워드 추출 함수 (단순 문자열 분리)
def extract_keywords(text):
    words = text.split()
    keywords = [word for word in words if len(word) > 1 and word not in ["환자", "검사", "증상", "및", "또는", "있습니다"]]
    return keywords

# JSON 파일이 있는 디렉토리 경로
base_dir = "/Users/jamie/Desktop/09.필수의료 의학지식 데이터/3.개방데이터/1.데이터/Training/02.라벨링데이터"
folders = ["TL_내과", "TL_산부인과", "TL_소아청소년과", "TL_응급의학과"]

# 각 폴더에서 JSON 파일 처리
for folder in folders:
    folder_path = os.path.join(base_dir, folder)
    if not os.path.exists(folder_path):
        print(f"폴더를 찾을 수 없습니다: {folder_path}")
        continue
    
    print(f"폴더 처리 중: {folder_path}")
    files = os.listdir(folder_path)
    print(f"파일 목록: {files}")
    
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(folder_path, file)
            try:
                with open(file_path, "r", encoding="utf-8-sig") as f:  # utf-8-sig로 변경
                    data = json.load(f)
                    # 키워드 추출
                    question = data["question"]
                    keywords = extract_keywords(question)
                    # MongoDB에 저장할 데이터 구조
                    processed_data = {
                        "qa_id": data["qa_id"],
                        "question": question,
                        "keywords": keywords,
                        "answer": data["answer"],
                        "department": folder[3:]  # 폴더 이름에서 진료과 추출 (예: "TL_내과" → "내과")
                    }
                    collection.insert_one(processed_data)
                    print(f"업로드 완료: {file_path}")
            except Exception as e:
                print(f"파일 처리 오류: {file_path}, 오류: {e}")

# 키워드 인덱스 생성
collection.create_index([("keywords", 1)])
print("데이터 업로드 및 인덱스 생성 완료!")
print(f"업로드된 데이터 개수: {collection.count_documents({})}")