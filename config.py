"""
설정 관리 모듈
환경변수를 통해 애플리케이션 설정을 관리합니다.
"""

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Settings:
    """애플리케이션 설정 클래스"""
    
    # 서버 설정
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # OpenAI 설정
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Google Gemini 설정
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_MODEL: str = os.getenv("GOOGLE_MODEL", "gemini-pro")
    
    # LLM 제공자 설정
    DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", "openai")
    
    # 외부 서비스 API 설정
    EXTERNAL_API_BASE_URL: str = os.getenv("EXTERNAL_API_BASE_URL", "")
    EXTERNAL_API_TOKEN: str = os.getenv("EXTERNAL_API_TOKEN", "")

    # 개발모드 설정
    DEV_MODE: bool = os.getenv("DEV_MODE", "True").lower() == "true"
    DEV_USER_ID: str = os.getenv("DEV_USER_ID", "dev_user_id_for_testing")
    
    # 스케줄링 설정 (더 활발한 커뮤니티를 위한 짧은 간격)
    COMMENT_MIN_INTERVAL_MINUTES: int = int(os.getenv("COMMENT_MIN_INTERVAL_MINUTES", "1"))   # 댓글: 최소 1분
    COMMENT_MAX_INTERVAL_MINUTES: int = int(os.getenv("COMMENT_MAX_INTERVAL_MINUTES", "3"))   # 댓글: 최대 3분
    POST_MIN_INTERVAL_MINUTES: int = int(os.getenv("POST_MIN_INTERVAL_MINUTES", "1"))        # 게시글: 최소 1분
    POST_MAX_INTERVAL_MINUTES: int = int(os.getenv("POST_MAX_INTERVAL_MINUTES", "5"))        # 게시글: 최대 5분

# 전역 설정 인스턴스
settings = Settings()
