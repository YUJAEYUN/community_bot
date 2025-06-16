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
- 댓글: 30분 ~ 10시간 랜덤 간격
- 게시글: 24시간 ~ 72시간 랜덤 간격
- APScheduler를 통한 백그라운드 자동 실행

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

## 설치 및 실행

### 1. 가상환경 생성 및 활성화
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정
`.env` 파일에서 다음 값들을 설정하세요:
```env
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
EXTERNAL_API_BASE_URL=https://your-service-api.com
EXTERNAL_API_TOKEN=your_external_api_token
```

### 4. 서버 실행
```bash
python main.py
```

또는

```bash
uvicorn main:app --reload
```

서버는 기본적으로 `http://localhost:8000`에서 실행됩니다.

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

## 주의사항

1. **API 키 보안**: `.env` 파일의 API 키들을 안전하게 관리하세요.
2. **부정적 피드 필터링**: 시스템이 자동으로 부정적인 피드를 감지하여 댓글 생성을 차단합니다.
3. **외부 API 연동**: 실제 서비스 연동을 위해서는 `scheduler_service.py`의 외부 API 호출 부분을 구현해야 합니다.

## 개발 및 확장

- 새로운 LLM 모델 추가: `services/llm_service.py` 수정
- 스케줄링 로직 변경: `services/scheduler_service.py` 수정
- 새로운 API 엔드포인트 추가: `main.py` 수정

## 라이선스

이 프로젝트는 커뮤니티 활성화를 위한 사회 실험적 성격을 띠고 있습니다.
