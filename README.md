# Community Bot API

소개팅 앱 커뮤니티 활성화를 위한 AI 댓글 및 게시글 생성 백엔드 서버

## 프로젝트 개요

이 프로젝트는 소개팅 앱 커뮤니티의 활성화를 위해 AI가 자동으로 댓글과 게시글을 생성하는 백엔드 서버입니다. LangChain을 활용하여 감성 분석을 통한 부정적 피드 필터링과 긍정적인 댓글/게시글 생성 기능을 제공합니다.

## 주요 기능

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
│   └── scheduler_service.py # 스케줄링 서비스
└── utils/
    ├── __init__.py
    └── random_generator.py # 랜덤 닉네임/대학명 생성
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

## 🔧 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Community     │    │   Dating App    │    │   OpenAI API    │
│   Bot Server    │◄──►│   Backend       │    │                 │
│   (FastAPI)     │    │   (Spring)      │    │   (GPT-4)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                       │
    ┌────▼────┐             ┌────▼────┐
    │ AI 게시글 │             │ AI 댓글  │
    │ 자동생성  │             │ 자동생성  │
    └─────────┘             └─────────┘
```

## 📊 현재 설정

- **댓글 생성**: 1분 ~ 1시간 간격
- **게시글 생성**: 10분 ~ 2시간 간격
- **AI 엔드포인트**: `/api/ai/content/articles`, `/api/ai/content/articles/{id}/comments`
- **랜덤 닉네임**: 매번 다른 익명 사용자로 생성

## 🚀 고도화된 기능 상세

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
- **스케줄링 로직**: `services/scheduler_service.py` 수정
- **API 엔드포인트**: `main.py` 수정
- **프롬프트 튜닝**: 각 프롬프트 템플릿 수정

## 라이선스

이 프로젝트는 커뮤니티 활성화를 위한 사회 실험적 성격을 띠고 있습니다.
