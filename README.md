# Community Bot API

소개팅 앱 커뮤니티 활성화를 위한 AI 댓글 및 게시글 생성 백엔드 서버

## 프로젝트 개요

이 프로젝트는 소개팅 앱 커뮤니티의 활성화를 위해 AI가 자동으로 댓글과 게시글을 생성하는 백엔드 서버입니다. LangChain을 활용하여 감성 분석을 통한 부정적 피드 필터링과 긍정적인 댓글/게시글 생성 기능을 제공하며, **RAG(Retrieval-Augmented Generation) 시스템**을 통해 실제 커뮤니티 데이터를 학습하여 더욱 자연스럽고 맥락에 맞는 콘텐츠를 생성합니다.

## 주요 기능

### 🧠 RAG 기반 지능형 콘텐츠 생성
- **커뮤니티 데이터 임베딩**: 실제 커뮤니티 글/댓글을 벡터 데이터베이스에 저장
- **맥락 인식 검색**: 게시글과 댓글의 맥락을 파악하여 유사한 과거 데이터 검색
- **퓨샷 학습**: 검색된 데이터를 LLM 컨텍스트에 추가하여 더 자연스러운 응답 생성
- **수동 데이터 관리**: 새로운 트렌드와 유행어를 필요에 따라 수동으로 업데이트
- **품질 향상**: 실제 사용자 어투, 감성, 문화를 반영한 '사람 같은' 콘텐츠

### 🤖 고도화된 AI 댓글 생성
- **페르소나 기반 댓글**: 5가지 다양한 성격의 AI 페르소나가 자연스러운 댓글 생성
- **컨텍스트 인식**: 피드 내용을 분석하여 질문, 감정, 주제에 맞는 적절한 반응
- **고급 감성 분석**: 부정적 피드 정밀 필터링 (매칭 불만, 외모 비하, 서비스 불만 등)
- **품질 검증**: 댓글 길이, 적절성 자동 검증 및 정리
- **실제 대학생 스타일**: 자연스러운 말투, 이모티콘, 줄임말 사용

### 🎯 스마트 게시글 생성
- **카테고리별 특화**: 실시간/리뷰/연애상담 카테고리별 맞춤 게시글
- **페르소나 다양성**: 친근한/차분한/유머러스한/진지한/감성적인 5가지 성격
- **현실적 내용**: 실제 대학생이 쓸 법한 구체적이고 자연스러운 내용
- **참여 유도**: 댓글을 유도하는 자연스러운 질문으로 마무리

### 🧠 지능형 감성 분석
- **다층 분석**: 감정, 의도, 맥락을 종합적으로 고려
- **세밀한 필터링**: 70% 감정, 20% 키워드, 10% 커뮤니티 영향 고려
- **상세 정보**: 감지된 감정과 주요 주제 정보 제공
- **안전 장치**: 오류 시 안전하게 부정적으로 분류

### ⚡ 자동 스케줄링
- **댓글**: 1분 ~ 1시간 랜덤 간격
- **게시글**: 10분 ~ 2시간 랜덤 간격
- **APScheduler**: 백그라운드 자동 실행
- **오류 복구**: 실패 시 자동 재시도 및 다음 스케줄 예약

### 🎭 AI 페르소나 시스템
1. **친근하고 활발한**: 밝고 에너지 넘치는 말투, 이모티콘 적극 활용
2. **차분하고 따뜻한**: 정중하고 공감적인 말투, 부드러운 표현
3. **유머러스하고 재치있는**: 위트 있고 장난스러운 말투, 적절한 농담
4. **진지하고 신중한**: 차분하고 논리적인 말투, 깊이 있는 조언
5. **감성적이고 로맨틱한**: 감성적이고 시적인 표현, 따뜻한 말투

## 기술 스택

- **백엔드**: FastAPI
- **LLM**: LangChain + OpenAI GPT / Google Gemini
- **RAG 시스템**: LangChain + Vector Database (Chroma/FAISS)
- **임베딩**: OpenAI Embeddings / HuggingFace Embeddings
- **벡터 검색**: 유사도 기반 의미 검색
- **스케줄링**: APScheduler
- **환경 관리**: python-dotenv

## 프로젝트 구조

```
community_bot/
├── main.py                 # FastAPI 메인 서버
├── config.py              # 설정 관리
├── requirements.txt       # 의존성 패키지
├── .env                   # 환경변수 (API 키 등)
├── models/
│   ├── __init__.py
│   └── schemas.py         # Pydantic 데이터 모델
├── services/
│   ├── __init__.py
│   ├── llm_service.py     # LangChain LLM 서비스
│   ├── rag_service.py     # RAG 시스템 서비스
│   ├── embedding_service.py # 임베딩 및 벡터 DB 서비스
│   ├── scheduler_service.py # 스케줄링 서비스
│   └── external_api_service.py # 외부 API 연동
├── utils/
│   ├── __init__.py
│   ├── random_generator.py # 랜덤 닉네임/대학명 생성
│   └── data_processor.py  # 데이터 전처리 유틸리티
├── data/
│   ├── raw/               # 원본 커뮤니티 데이터
│   ├── processed/         # 전처리된 데이터
│   └── embeddings/        # 임베딩 벡터 저장소
└── vector_db/             # 벡터 데이터베이스 저장소
```

## 🚀 설치 및 실행

### 1️⃣ 프로젝트 클론 및 디렉토리 이동
```bash
git clone <repository-url>
cd community_bot
```

### 2️⃣ 가상환경 생성 및 활성화
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3️⃣ 의존성 설치
```bash
pip install -r requirements.txt
```

### 4️⃣ 환경변수 설정
`.env` 파일을 생성하고 다음 값들을 설정하세요:
```env
# OpenAI API 설정
OPENAI_API_KEY=your_openai_api_key_here

# 외부 서비스 API 엔드포인트 (소개팅 서비스 백엔드)
EXTERNAL_API_BASE_URL=http://localhost:8044/api
EXTERNAL_API_TOKEN=your_jwt_token_here

# RAG 시스템 설정
VECTOR_DB_TYPE=chroma                # 벡터 DB 타입 (chroma/faiss)
VECTOR_DB_PATH=./vector_db           # 벡터 DB 저장 경로
EMBEDDING_MODEL=text-embedding-ada-002  # 임베딩 모델
CHUNK_SIZE=500                       # 텍스트 청크 크기
CHUNK_OVERLAP=50                     # 청크 오버랩 크기
SIMILARITY_THRESHOLD=0.7             # 유사도 임계값

# 스케줄링 설정
COMMENT_MIN_INTERVAL_MINUTES=1       # 댓글: 최소 1분
COMMENT_MAX_INTERVAL_HOURS=1         # 댓글: 최대 1시간
POST_MIN_INTERVAL_MINUTES=10         # 게시글: 최소 10분
POST_MAX_INTERVAL_HOURS=2            # 게시글: 최대 2시간

# 개발 모드 설정
DEV_MODE=false
DEV_USER_ID=dev-user-123
```

### 5️⃣ 서버 실행
```bash
# 개발 모드 (자동 리로드)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 또는 간단히
python main.py
```

### 6️⃣ 서버 실행 확인
브라우저에서 다음 URL들로 접속해서 확인:
- **API 문서**: http://localhost:8000/docs
- **헬스체크**: http://localhost:8000/health
- **스케줄러 상태**: http://localhost:8000/scheduler/status

---

## 📋 주요 명령어

### 서버 관리
```bash
# 서버 시작
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 서버 종료 (Ctrl+C 또는)
pkill -f uvicorn

# 백그라운드 실행
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
```

### 스케줄러 관리
```bash
# 스케줄러 재시작
curl -X POST "http://localhost:8000/scheduler/restart"

# 수동 게시글 생성
curl -X POST "http://localhost:8000/scheduler/trigger-post"

# 수동 댓글 생성
curl -X POST "http://localhost:8000/scheduler/trigger-comment"
```

### 문제 해결
```bash
# 포트 충돌 시 - 8000번 포트 사용 중인 프로세스 확인
lsof -i :8000

# 프로세스 종료
kill -9 <PID>

# 가상환경 재생성
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## API 엔드포인트

### 기본 정보
- `GET /` - 서버 정보
- `GET /health` - 헬스 체크
- `GET /docs` - Swagger UI 문서

### 댓글/게시글 생성
- `POST /analyze-sentiment` - 피드 감성 분석
- `POST /generate-comment` - AI 댓글 생성
- `POST /generate-post` - AI 게시글 생성

### RAG 시스템 관리
- `POST /rag/upload-data` - 커뮤니티 데이터 업로드 및 임베딩
- `POST /rag/search` - 유사 콘텐츠 검색
- `GET /rag/status` - RAG 시스템 상태 조회
- `DELETE /rag/clear` - 벡터 DB 초기화

### 스케줄러 관리
- `GET /scheduler/status` - 스케줄러 상태 조회
- `POST /scheduler/start` - 스케줄러 시작
- `POST /scheduler/stop` - 스케줄러 중지
- `POST /scheduler/restart` - 스케줄러 재시작
- `POST /scheduler/trigger-post` - 수동 게시글 생성
- `POST /scheduler/trigger-comment` - 수동 댓글 생성

### 외부 API 테스트
- `POST /external-api/test-article` - 외부 API 게시글 생성 테스트
- `POST /external-api/test-comment` - 외부 API 댓글 생성 테스트

## 🧪 테스트

### 고도화된 LLM 기능 테스트
```bash
# 전체 기능 테스트 (감성 분석, 댓글 생성, 게시글 생성)
python test_enhanced_llm.py
```

### 개별 기능 테스트
```bash
# 감성 분석 테스트
curl -X POST "http://localhost:8000/analyze-sentiment" \
  -H "Content-Type: application/json" \
  -d '{"feed_content": "오늘 카페에서 공부했는데 분위기가 너무 좋았어요!"}'

# 페르소나 기반 댓글 생성 테스트
curl -X POST "http://localhost:8000/generate-comment" \
  -H "Content-Type: application/json" \
  -d '{"feed_content": "요즘 과제 때문에 스트레스가 너무 심해요..."}'

# 카테고리별 게시글 생성 테스트
curl -X POST "http://localhost:8000/generate-post" \
  -H "Content-Type: application/json" \
  -d '{"topic": "review"}'

# RAG 시스템 테스트
curl -X POST "http://localhost:8000/rag/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "카페 추천", "limit": 5}'
```

## 사용 예시

### 댓글 생성
```bash
curl -X POST "http://localhost:8000/generate-comment" \
  -H "Content-Type: application/json" \
  -d '{"feed_content": "오늘 카페에서 공부하는데 집중이 잘 안 되네요"}'
```

### 게시글 생성
```bash
curl -X POST "http://localhost:8000/generate-post" \
  -H "Content-Type: application/json" \
  -d '{"topic": "주말 데이트 코스"}'
```

## ⚠️ 주의사항

1. **API 키 보안**: `.env` 파일의 API 키들을 안전하게 관리하세요.
2. **부정적 피드 필터링**: 시스템이 자동으로 부정적인 피드를 감지하여 댓글 생성을 차단합니다.
3. **AI 전용 엔드포인트**: 다양한 닉네임 생성을 위해 `/api/ai/content/` 엔드포인트를 사용합니다.
4. **서비스 백엔드 연동**: 소개팅 서비스 백엔드가 실행 중이어야 정상 작동합니다.
5. **스케줄링 간격**: 너무 짧은 간격 설정 시 API 호출 제한에 걸릴 수 있습니다.
6. **RAG 데이터 관리**:
   - 커뮤니티 데이터 수집 시 해당 서비스의 약관 및 정책을 준수하세요
   - 개인정보가 포함된 데이터는 반드시 익명화 처리하세요
   - 부적절한 콘텐츠는 사전에 필터링하여 업로드하세요
7. **벡터 DB 용량**: 대량의 데이터 임베딩 시 충분한 저장 공간을 확보하세요.
8. **임베딩 비용**: OpenAI Embeddings API 사용 시 토큰 사용량에 따른 비용이 발생합니다.

## 🔧 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Community     │    │   Dating App    │    │   OpenAI API    │
│   Bot Server    │◄──►│   Backend       │    │   (GPT-4 +      │
│   (FastAPI)     │    │   (Spring)      │    │   Embeddings)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
    ┌────▼────┐             ┌────▼────┐             ┌────▼────┐
    │ AI 게시글 │             │ AI 댓글  │             │ RAG 시스템│
    │ 자동생성  │             │ 자동생성  │             │ (벡터 DB) │
    └─────────┘             └─────────┘             └─────────┘
                                   │                       │
                                   │                       │
                              ┌────▼───────────────────────▼────┐
                              │     맥락 인식 콘텐츠 생성        │
                              │  (과거 데이터 기반 퓨샷 학습)    │
                              └─────────────────────────────────┘
```

## 📊 현재 설정

- **댓글 생성**: 1분 ~ 1시간 간격
- **게시글 생성**: 10분 ~ 2시간 간격
- **AI 엔드포인트**: `/api/ai/content/articles`, `/api/ai/content/articles/{id}/comments`
- **랜덤 닉네임**: 매번 다른 익명 사용자로 생성
- **RAG 시스템**:
  - 벡터 DB: Chroma (기본값)
  - 임베딩 모델: text-embedding-ada-002
  - 청크 크기: 500자
  - 유사도 임계값: 0.7

## 🚀 고도화된 기능 상세

### 🧠 RAG 시스템 (Retrieval-Augmented Generation)
실제 커뮤니티 데이터를 활용하여 더욱 자연스럽고 맥락에 맞는 콘텐츠를 생성합니다.

#### 작동 원리
1. **데이터 수집**: 실제 커뮤니티 글/댓글 데이터를 수집
2. **전처리**: 텍스트 정제, 청크 분할, 메타데이터 추출
3. **임베딩**: OpenAI Embeddings를 사용하여 벡터화
4. **저장**: Chroma/FAISS 벡터 데이터베이스에 저장
5. **검색**: 새로운 콘텐츠 생성 시 유사한 과거 데이터 검색
6. **생성**: 검색된 데이터를 컨텍스트로 활용하여 LLM 응답 생성

#### 장점
- **품질 향상**: 실제 사용자 어투, 유행어, 감성 반영
- **일관성 유지**: 커뮤니티 특정 분위기와 문화 유지
- **맥락 인식**: 게시글과 댓글 간의 관계 파악
- **비용 효율성**: 웹 검색 대비 빠르고 저렴한 검색
- **통제 가능성**: 특정 커뮤니티 데이터만 사용하여 품질 관리

#### 데이터 관리
- **수동 업데이트**: 새로운 트렌드나 유행어를 필요에 따라 추가
- **품질 관리**: 부적절한 콘텐츠 필터링 및 정제
- **버전 관리**: 데이터셋 변경 이력 추적

### 페르소나 시스템
각 AI 페르소나는 고유한 성격, 말투, 관심사, 글쓰기 스타일을 가지고 있어 더욱 자연스럽고 다양한 응답을 생성합니다.

### 컨텍스트 인식
- **질문 감지**: 물음표나 의문사 포함 여부 분석
- **감정 표현**: 이모티콘이나 감정 단어 감지
- **주제 분류**: 연애, 음식, 취미 등 주제별 맞춤 반응
- **길이 고려**: 피드 길이에 따른 적절한 댓글 생성

### 품질 검증 시스템
- **길이 제한**: 댓글 150자, 게시글 500자 제한
- **부적절 표현 필터링**: 자동 감지 및 대체
- **JSON 파싱 오류 처리**: 정규식 백업 파싱
- **폴백 시스템**: 오류 시 안전한 기본 응답 제공

### 카테고리별 특화
- **실시간**: 지금 당장의 고민이나 궁금증
- **리뷰**: 구체적인 장소명과 솔직한 후기
- **연애상담**: 현실적이고 공감 가능한 상황

## 개발 및 확장

### RAG 데이터 관리

#### 새로운 데이터 추가
```bash
# 1. 데이터 파일을 data/raw/ 디렉토리에 저장
# 2. API를 통해 데이터 업로드 및 임베딩
curl -X POST "http://localhost:8000/rag/upload-data" \
  -H "Content-Type: application/json" \
  -d '{"file_path": "data/raw/new_community_data.json"}'
```

#### 데이터 형식
```json
{
  "posts": [
    {
      "id": "post_001",
      "title": "게시글 제목",
      "content": "게시글 내용",
      "category": "general",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "comments": [
    {
      "id": "comment_001",
      "post_id": "post_001",
      "content": "댓글 내용",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### 새로운 페르소나 추가
```python
# services/llm_service.py의 PERSONAS 리스트에 추가
PersonaConfig(
    personality="새로운 성격",
    tone="새로운 말투",
    interests=["관심사1", "관심사2"],
    writing_style="새로운 글쓰기 스타일"
)
```

### 새로운 카테고리 추가
```python
# generate_post 메서드의 category_guides에 추가
"new_category": {
    "category": "새 카테고리",
    "guide": "새로운 가이드 내용"
}
```

### 커스터마이징
- **새로운 LLM 모델**: `services/llm_service.py` 수정
- **RAG 시스템**: `services/rag_service.py`, `services/embedding_service.py` 수정
- **스케줄링 로직**: `services/scheduler_service.py` 수정
- **API 엔드포인트**: `main.py` 수정
- **프롬프트 튜닝**: 각 프롬프트 템플릿 수정

## 라이선스

이 프로젝트는 커뮤니티 활성화를 위한 사회 실험적 성격을 띠고 있습니다.
