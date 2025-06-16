"""
소개팅 앱 커뮤니티 AI 댓글/게시글 생성 백엔드 서버
FastAPI를 사용하여 RESTful API를 제공합니다.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
import uvicorn
import logging

from config import settings
from models.schemas import (
    CommentRequest, CommentResponse, PostRequest, PostResponse,
    SentimentAnalysisResult, ScheduleStatus
)
from services.llm_service import llm_service
from services.scheduler_service import scheduler_service
from services.external_api_service import external_api_service, ArticleType
from utils.random_generator import generate_comment_signature, generate_post_signature

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시 실행
    logger.info("애플리케이션 시작 중...")
    scheduler_service.start()
    yield
    # 종료 시 실행
    logger.info("애플리케이션 종료 중...")
    scheduler_service.stop()

# FastAPI 앱 생성
app = FastAPI(
    title="Community Bot API",
    description="소개팅 앱 커뮤니티 활성화를 위한 AI 댓글/게시글 생성 서비스",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 시에는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Community Bot API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "scheduler_running": scheduler_service.is_running
    }

@app.post("/analyze-sentiment", response_model=SentimentAnalysisResult)
async def analyze_sentiment(feed_content: str):
    """
    피드 내용의 감성을 분석합니다.
    
    Args:
        feed_content (str): 분석할 피드 내용
        
    Returns:
        SentimentAnalysisResult: 감성 분석 결과
    """
    try:
        result = await llm_service.analyze_sentiment(feed_content)
        return result
    except Exception as e:
        logger.error(f"감성 분석 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="감성 분석 중 오류가 발생했습니다.")

@app.post("/generate-comment", response_model=CommentResponse)
async def generate_comment(request: CommentRequest):
    """
    피드에 대한 AI 댓글을 생성합니다.
    부정적인 피드에는 댓글을 생성하지 않습니다.
    
    Args:
        request (CommentRequest): 댓글 생성 요청
        
    Returns:
        CommentResponse: 생성된 댓글 정보
    """
    try:
        # 감성 분석 먼저 수행
        sentiment_result = await llm_service.analyze_sentiment(request.feed_content)
        
        if not sentiment_result.is_positive:
            raise HTTPException(
                status_code=400, 
                detail=f"부정적인 피드로 판단되어 댓글을 생성하지 않습니다. 사유: {sentiment_result.reason}"
            )
        
        # 댓글 생성
        comment = await llm_service.generate_comment(request.feed_content)
        comment_with_signature = generate_comment_signature(comment)
        
        # 작성자명 추출 (서명에서)
        author_name = comment_with_signature.split(" - ")[-1].replace(" 드림", "")
        
        return CommentResponse(
            comment=comment_with_signature,
            author_name=author_name,
            is_positive=sentiment_result.is_positive
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"댓글 생성 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="댓글 생성 중 오류가 발생했습니다.")

@app.post("/generate-post", response_model=PostResponse)
async def generate_post(request: PostRequest = PostRequest()):
    """
    커뮤니티 활성화를 위한 AI 게시글을 생성합니다.
    
    Args:
        request (PostRequest): 게시글 생성 요청
        
    Returns:
        PostResponse: 생성된 게시글 정보
    """
    try:
        # 게시글 생성
        title, content = await llm_service.generate_post(request.topic)
        post_signature = generate_post_signature()
        
        full_content = f"{content}\n\n{post_signature}"
        
        # 작성자명 추출 (서명에서)
        author_name = post_signature.replace("- ", "").replace(" 님의 질문", "")
        
        return PostResponse(
            title=title,
            content=full_content,
            author_name=author_name
        )
        
    except Exception as e:
        logger.error(f"게시글 생성 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="게시글 생성 중 오류가 발생했습니다.")

@app.get("/scheduler/status", response_model=ScheduleStatus)
async def get_scheduler_status():
    """
    스케줄러 상태를 조회합니다.
    
    Returns:
        ScheduleStatus: 스케줄러 상태 정보
    """
    try:
        status = scheduler_service.get_status()
        return ScheduleStatus(
            next_comment_time=status.get("next_comment_time"),
            next_post_time=status.get("next_post_time"),
            is_running=status.get("is_running", False)
        )
    except Exception as e:
        logger.error(f"스케줄러 상태 조회 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="스케줄러 상태 조회 중 오류가 발생했습니다.")

@app.post("/scheduler/start")
async def start_scheduler():
    """스케줄러를 시작합니다."""
    try:
        if not scheduler_service.is_running:
            scheduler_service.start()
            return {"message": "스케줄러가 시작되었습니다."}
        else:
            return {"message": "스케줄러가 이미 실행 중입니다."}
    except Exception as e:
        logger.error(f"스케줄러 시작 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="스케줄러 시작 중 오류가 발생했습니다.")

@app.post("/scheduler/stop")
async def stop_scheduler():
    """스케줄러를 중지합니다."""
    try:
        if scheduler_service.is_running:
            scheduler_service.stop()
            return {"message": "스케줄러가 중지되었습니다."}
        else:
            return {"message": "스케줄러가 이미 중지되어 있습니다."}
    except Exception as e:
        logger.error(f"스케줄러 중지 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="스케줄러 중지 중 오류가 발생했습니다.")

@app.post("/scheduler/restart")
async def restart_scheduler():
    """스케줄러를 재시작하여 새로운 설정을 즉시 적용합니다."""
    try:
        # 스케줄러 재시작
        scheduler_service.restart()
        logger.info("새로운 설정으로 스케줄러를 재시작했습니다.")

        return {
            "message": "스케줄러가 새로운 설정으로 재시작되었습니다.",
            "status": scheduler_service.get_status()
        }
    except Exception as e:
        logger.error(f"스케줄러 재시작 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="스케줄러 재시작 중 오류가 발생했습니다.")

@app.post("/scheduler/trigger-post")
async def trigger_post_now():
    """즉시 게시글을 생성합니다."""
    try:
        await scheduler_service._generate_auto_post()
        return {"message": "게시글이 즉시 생성되었습니다."}
    except Exception as e:
        logger.error(f"즉시 게시글 생성 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="즉시 게시글 생성 중 오류가 발생했습니다.")

@app.post("/scheduler/trigger-comment")
async def trigger_comment_now():
    """즉시 댓글을 생성합니다."""
    try:
        await scheduler_service._generate_auto_comment()
        return {"message": "댓글이 즉시 생성되었습니다."}
    except Exception as e:
        logger.error(f"즉시 댓글 생성 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="즉시 댓글 생성 중 오류가 발생했습니다.")

# 외부 API 테스트 엔드포인트들
@app.get("/external-api/articles")
async def get_external_articles(category: str = "general"):
    """외부 API에서 최근 게시글을 가져옵니다."""
    try:
        articles = await external_api_service.get_recent_articles(category, 5)
        return {"articles": articles, "count": len(articles) if articles else 0}
    except Exception as e:
        logger.error(f"외부 게시글 조회 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="외부 게시글 조회 중 오류가 발생했습니다.")

@app.post("/external-api/test-comment")
async def test_external_comment(article_id: str, content: str):
    """외부 API 댓글 작성을 테스트합니다."""
    try:
        result = await external_api_service.create_comment(
            article_id=article_id,
            content=content,
            anonymous=True
        )
        return {"success": result is not None, "result": result}
    except Exception as e:
        logger.error(f"외부 댓글 작성 테스트 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="외부 댓글 작성 테스트 중 오류가 발생했습니다.")

class TestArticleRequest(BaseModel):
    title: str
    content: str
    article_type: str = "general"

@app.post("/external-api/test-article")
async def test_external_article(request: TestArticleRequest):
    """외부 API 게시글 작성을 테스트합니다."""
    try:
        # 문자열을 ArticleType enum으로 변환
        try:
            type_enum = ArticleType(request.article_type)
        except ValueError:
            type_enum = ArticleType.GENERAL

        result = await external_api_service.create_article(
            title=request.title,
            content=request.content,
            article_type=type_enum,
            anonymous=True
        )
        return {"success": result is not None, "result": result}
    except Exception as e:
        logger.error(f"외부 게시글 작성 테스트 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="외부 게시글 작성 테스트 중 오류가 발생했습니다.")

@app.get("/external-api/test-connection")
async def test_external_connection():
    """외부 API 연결 상태를 테스트합니다."""
    try:
        # 개발모드 상태 확인
        return {
            "dev_mode": settings.DEV_MODE,
            "base_url": settings.EXTERNAL_API_BASE_URL,
            "has_token": bool(settings.EXTERNAL_API_TOKEN),
            "status": "ready"
        }
    except Exception as e:
        logger.error(f"연결 테스트 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="연결 테스트 중 오류가 발생했습니다.")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
