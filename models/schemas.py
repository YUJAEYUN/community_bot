"""
데이터 모델 정의
Pydantic을 사용하여 API 요청/응답 스키마를 정의합니다.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class FeedContent(BaseModel):
    """피드 내용 모델"""
    content: str = Field(..., description="피드 내용")
    author_id: Optional[str] = Field(None, description="작성자 ID")
    created_at: Optional[datetime] = Field(None, description="작성 시간")

class CommentRequest(BaseModel):
    """댓글 생성 요청 모델"""
    feed_content: str = Field(..., description="댓글을 달 피드 내용")
    feed_id: Optional[str] = Field(None, description="피드 ID")

class CommentResponse(BaseModel):
    """댓글 생성 응답 모델"""
    comment: str = Field(..., description="생성된 댓글")
    author_name: str = Field(..., description="댓글 작성자명 (랜덤 생성)")
    is_positive: bool = Field(..., description="긍정적 피드 여부")
    created_at: datetime = Field(default_factory=datetime.now, description="생성 시간")

class PostRequest(BaseModel):
    """게시글 생성 요청 모델"""
    topic: Optional[str] = Field(None, description="게시글 주제 (선택사항)")

class PostResponse(BaseModel):
    """게시글 생성 응답 모델"""
    title: str = Field(..., description="게시글 제목")
    content: str = Field(..., description="게시글 내용")
    author_name: str = Field(..., description="게시글 작성자명 (랜덤 생성)")
    created_at: datetime = Field(default_factory=datetime.now, description="생성 시간")

class SentimentAnalysisResult(BaseModel):
    """감성 분석 결과 모델"""
    is_positive: bool = Field(..., description="긍정적 내용 여부")
    confidence: float = Field(..., description="신뢰도 (0.0 ~ 1.0)")
    reason: str = Field(..., description="판단 근거")

class ScheduleStatus(BaseModel):
    """스케줄 상태 모델"""
    next_comment_time: Optional[datetime] = Field(None, description="다음 댓글 생성 시간")
    next_post_time: Optional[datetime] = Field(None, description="다음 게시글 생성 시간")
    is_running: bool = Field(..., description="스케줄러 실행 상태")
