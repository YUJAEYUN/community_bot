# Community Bot API

소개팅 앱 커뮤니티 활성화를 위한 AI 댓글 및 게시글 생성 백엔드 서버

## 프로젝트 개요

이 프로젝트는 소개팅 앱 커뮤니티의 활성화를 위해 AI가 자동으로 댓글과 게시글을 생성하는 백엔드 서버입니다. LangChain을 활용하여 감성 분석을 통한 부정적 피드 필터링과 긍정적인 댓글/게시글 생성 기능을 제공합니다.

## 주요 기능

### 1. AI 댓글 생성
- 사용자 피드에 대한 긍정적이고 공감적인 댓글 생성
- 부정적인 피드 자동 필터링 (매칭 불만, 외모 비하, 서비스 불만 등)
- 랜덤한 대학명, 닉네임, 숫자 조합으로 작성자명 생성

### 2. AI 게시글 생성
- 커뮤니티 활성화를 위한 흥미로운 주제의 게시글 생성
- 연애, 일상, 취미 등 긍정적인 내용 위주
- 랜덤한 작성자 정보 자동 생성

### 3. 자동 스케줄링
- 댓글: 1분 ~ 1시간 랜덤 간격
- 게시글: 10분 ~ 2시간 랜덤 간격
- APScheduler를 통한 백그라운드 자동 실행

### 4. AI 전용 엔드포인트
- 매번 다른 랜덤 닉네임으로 게시글/댓글 생성
- 서비스 백엔드의 AI 전용 API 활용
- 자연스러운 커뮤니티 활동 시뮬레이션

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

## 개발 및 확장

- 새로운 LLM 모델 추가: `services/llm_service.py` 수정
- 스케줄링 로직 변경: `services/scheduler_service.py` 수정
- 새로운 API 엔드포인트 추가: `main.py` 수정

## 라이선스

이 프로젝트는 커뮤니티 활성화를 위한 사회 실험적 성격을 띠고 있습니다.
