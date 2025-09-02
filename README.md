# 의학지식 탐구챗봇 (Medical Knowledge Explorer Chatbot) 💊

키워드 기반으로 의학 관련 질문과 정답을 검색할 수 있는 Streamlit 기반 챗봇입니다.

## 주요 기능

- 키워드 입력 시 관련 의학 질문 3개 자동 검색
- 4개 진료과 데이터 지원 (내과, 산부인과, 소아청소년과, 응급의학과)
- AI Hub 공개 데이터셋 활용으로 신뢰성 있는 의학 정보 제공
- MongoDB 기반 빠른 검색
- 직관적인 Streamlit UI

## 기술 스택

- **Frontend**: Streamlit
- **Database**: MongoDB
- **Language**: Python 3.9+
- **Libraries**: pymongo, streamlit

## 사전 준비사항

### 1. 데이터 준비
이 프로젝트는 **AI Hub의 필수의료 의학지식 데이터** 데이터셋을 사용합니다.

**데이터 다운로드**:
- 출처: [AI Hub - 필수의료 의학지식 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&searchKeyword=%ED%95%84%EC%88%98%EC%9D%98%EB%A3%8C%20%EC%9D%98%ED%95%99%EC%A7%80%EC%8B%9D%20%EB%8D%B0%EC%9D%B4%ED%84%B0&aihubDataSe=data&dataSetSn=71875)
- AI Hub 회원가입 후 데이터 신청 및 다운로드
- 데이터 다운로드 후 다음 구조로 배치:
```
프로젝트폴더/
├── 09.필수의료 의학지식 데이터/
│   └── 3.개방데이터/
│       └── 1.데이터/
│           └── Training/
│               └── 02.라벨링데이터/
│                   ├── TL_내과/
│                   ├── TL_산부인과/
│                   ├── TL_소아청소년과/
│                   └── TL_응급의학과/
```

### 2. MongoDB 설치
```bash
# macOS (Homebrew)
brew tap mongodb/brew
brew install mongodb-community

# Ubuntu
sudo apt-get install mongodb

# Windows
# MongoDB 공식 사이트에서 다운로드
```

## 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/Jamie-Kang/medical-knowledge-chatbot.git
cd medical-knowledge-chatbot
```

### 2. 가상환경 설정
```bash
# Conda 사용
conda create -n medical python=3.9
conda activate medical

# 또는 venv 사용
python -m venv medical
source medical/bin/activate  # macOS/Linux
# medical\Scripts\activate  # Windows
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. MongoDB 실행
```bash
# MongoDB 서비스 시작
brew services start mongodb/brew/mongodb-community  # macOS
sudo systemctl start mongod  # Ubuntu
```

### 5. 데이터 전처리 및 업로드
```bash
python preprocess_and_upload.py
```

### 6. 챗봇 실행
```bash
streamlit run studybot.py
```

브라우저에서 `http://localhost:8501` 접속

## 프로젝트 구조

```
medical-knowledge-chatbot/
├── README.md
├── requirements.txt
├── preprocess_and_upload.py    # 데이터 전처리 및 MongoDB 업로드
└── studybot.py                 # Streamlit 챗봇 메인 앱
```

## 🔧 설정

`preprocess_and_upload.py` 파일에서 다음 경로를 본인 환경에 맞게 수정하세요:

```python
# 데이터 경로 수정 (26번째 줄 근처)
base_dir = "/Users/jamie/Desktop/09.필수의료 의학지식 데이터/3.개방데이터/1.데이터/Training/02.라벨링데이터"
# ↓ 본인 경로로 변경
base_dir = "your/path/to/09.필수의료 의학지식 데이터/3.개방데이터/1.데이터/Training/02.라벨링데이터"
```

## 사용법

1. 챗봇 실행 후 키워드 입력창에 의학 관련 키워드 입력
2. 예시 키워드: `기침`, `칼슘 보충제`, `두통`, `발열` 등
3. 관련 질문 3개와 정답이 진료과별로 표시됨

## 데이터 구조

**데이터 출처**: AI Hub - 필수의료 의학지식 데이터  
**데이터 규모**: 4개 진료과별 질문-답변 쌍

각 JSON 파일은 다음과 같은 구조를 가집니다:

```json
{
  "qa_id": "질문답변 고유ID",
  "question": "의학 관련 질문",
  "answer": "해당 질문의 상세한 답변"
}
```

MongoDB에 저장되는 데이터 구조:
```json
{
  "qa_id": "sample_001",
  "question": "기침이 지속될 때 주의사항은?",
  "keywords": ["기침", "지속", "주의사항"],
  "answer": "기침이 2주 이상 지속되면 전문의 상담이 필요합니다...",
  "department": "내과"
}
```

##  키워드 검색 로직

- 입력 텍스트를 공백으로 분리하여 키워드 추출
- 길이 2 이상의 단어만 키워드로 인식
- 일반적인 불용어 제거 ("환자", "검사", "증상", "및", "또는", "있습니다")
- MongoDB의 `$in` 연산자로 키워드 매칭


- **데이터 출처**: [AI Hub - 필수의료 의학지식 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&searchKeyword=%ED%95%84%EC%88%98%EC%9D%98%EB%A3%8C%20%EC%9D%98%ED%95%99%EC%A7%80%EC%8B%9D%20%EB%8D%B0%EC%9D%B4%ED%84%B0&aihubDataSe=data&dataSetSn=71875)
- **데이터 사용**: AI Hub의 이용약관을 준수하여 사용
