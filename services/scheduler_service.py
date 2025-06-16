"""
APScheduler를 활용한 자동 댓글/게시글 생성 스케줄링 서비스
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
import asyncio
import logging
import random

from config import settings
from services.llm_service import llm_service
from services.external_api_service import external_api_service, ArticleType
from utils.random_generator import generate_comment_signature, generate_post_signature, get_random_interval_minutes

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SchedulerService:
    """스케줄링 서비스 클래스"""
    
    def __init__(self):
        """스케줄러 서비스 초기화"""
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
        
        # 샘플 피드 데이터 (실제 환경에서는 외부 API에서 가져옴)
        self.sample_feeds = [
            "오늘 카페에서 공부하는데 집중이 잘 안 되네요 ㅠㅠ",
            "주말에 뭐 하면 좋을까요? 추천 부탁드려요!",
            "새로운 취미를 시작하고 싶은데 뭐가 좋을까요?",
            "오늘 날씨가 정말 좋네요! 산책하기 딱 좋은 날씨예요",
            "요즘 운동을 시작했는데 생각보다 재미있어요",
            "맛있는 음식점 추천해주세요! 혼자 가기 좋은 곳으로요"
        ]
    
    def start(self):
        """스케줄러 시작"""
        if not self.is_running:
            self._schedule_next_comment()
            self._schedule_next_post()
            self.scheduler.start()
            self.is_running = True
            logger.info("스케줄러가 시작되었습니다.")

    def stop(self):
        """스케줄러 중지"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("스케줄러가 중지되었습니다.")

    def restart(self):
        """스케줄러 재시작 (새로운 설정 적용)"""
        # 기존 스케줄러 중지
        if self.is_running:
            self.stop()

        # 새 스케줄러 인스턴스 생성
        self.scheduler = AsyncIOScheduler()
        self.is_running = False

        # 새로운 설정으로 시작
        self.start()
    
    def _schedule_next_comment(self):
        """다음 댓글 생성 스케줄링"""
        # 랜덤 간격 계산 (30분 ~ 10시간)
        interval_minutes = get_random_interval_minutes(
            settings.COMMENT_MIN_INTERVAL_MINUTES,
            settings.COMMENT_MAX_INTERVAL_HOURS
        )
        
        run_time = datetime.now() + timedelta(minutes=interval_minutes)
        
        self.scheduler.add_job(
            self._generate_auto_comment,
            trigger='date',
            run_date=run_time,
            id=f'auto_comment_{datetime.now().timestamp()}',
            replace_existing=True
        )
        
        logger.info(f"다음 댓글 생성이 {run_time.strftime('%Y-%m-%d %H:%M:%S')}에 예약되었습니다.")
    
    def _schedule_next_post(self):
        """다음 게시글 생성 스케줄링"""
        # 랜덤 간격 계산 (10분 ~ 2시간)
        min_minutes = 10  # 10분
        max_minutes = settings.POST_MAX_INTERVAL_HOURS * 60  # 2시간 = 120분
        interval_minutes = random.randint(min_minutes, max_minutes)
        
        run_time = datetime.now() + timedelta(minutes=interval_minutes)
        
        self.scheduler.add_job(
            self._generate_auto_post,
            trigger='date',
            run_date=run_time,
            id=f'auto_post_{datetime.now().timestamp()}',
            replace_existing=True
        )
        
        logger.info(f"다음 게시글 생성이 {run_time.strftime('%Y-%m-%d %H:%M:%S')}에 예약되었습니다.")
    
    async def _generate_auto_comment(self):
        """자동 댓글 생성 및 전송"""
        try:
            # 1. 최근 게시글 목록 가져오기
            recent_articles = await external_api_service.get_recent_articles("general", 5)

            if not recent_articles:
                logger.warning("최근 게시글을 가져올 수 없어 샘플 피드를 사용합니다.")
                # 샘플 피드 사용
                feed_content = random.choice(self.sample_feeds)
                article_id = "sample_article_id"
            else:
                # 랜덤하게 게시글 선택
                selected_article = random.choice(recent_articles)
                feed_content = selected_article.get('content', '')
                article_id = selected_article.get('id', '')

                if not feed_content:
                    logger.warning("선택된 게시글에 내용이 없어 샘플 피드를 사용합니다.")
                    feed_content = random.choice(self.sample_feeds)
                    article_id = "sample_article_id"

            # 2. 감성 분석
            sentiment_result = await llm_service.analyze_sentiment(feed_content)

            if sentiment_result.is_positive:
                # 3. 긍정적인 피드에만 댓글 생성
                comment = await llm_service.generate_comment(feed_content)

                # 서명 제거 (외부 API에서는 순수 댓글 내용만 전송)
                clean_comment = comment.strip()

                # 4. 외부 API로 댓글 전송
                result = await external_api_service.create_comment(
                    article_id=article_id,
                    content=clean_comment,
                    anonymous=True
                )

                if result:
                    logger.info(f"자동 댓글 생성 완료 - 게시글 ID: {article_id}, 댓글: {clean_comment}")
                else:
                    logger.error(f"댓글 전송 실패 - 게시글 ID: {article_id}")
            else:
                logger.info(f"부정적인 피드로 판단되어 댓글을 생성하지 않습니다: {sentiment_result.reason}")

            # 5. 다음 댓글 스케줄링
            self._schedule_next_comment()

        except Exception as e:
            logger.error(f"자동 댓글 생성 중 오류 발생: {str(e)}")
            # 오류 발생 시에도 다음 스케줄 예약
            self._schedule_next_comment()
    
    async def _generate_auto_post(self):
        """자동 게시글 생성 및 전송"""
        try:
            # 1. 랜덤하게 게시글 타입 선택
            article_type = self._get_random_article_type()

            # 2. 선택된 타입에 맞는 게시글 생성
            title, content = await llm_service.generate_post(article_type=article_type.value)

            # 3. 외부 API로 게시글 전송 (anonymous는 항상 True)
            result = await external_api_service.create_article(
                title=title,
                content=content,
                article_type=article_type,
                anonymous=True
            )

            if result:
                logger.info(f"자동 게시글 생성 완료 - 타입: {article_type.value}, 제목: {title}, ID: {result.get('id')}")
            else:
                logger.error(f"게시글 전송 실패 - 타입: {article_type.value}, 제목: {title}")

            # 4. 다음 게시글 스케줄링
            self._schedule_next_post()

        except Exception as e:
            logger.error(f"자동 게시글 생성 중 오류 발생: {str(e)}")
            # 오류 발생 시에도 다음 스케줄 예약
            self._schedule_next_post()

    def _get_random_article_type(self) -> ArticleType:
        """
        랜덤하게 게시글 타입을 선택합니다.

        Returns:
            ArticleType: 랜덤 선택된 게시글 타입
        """
        # 3개 카테고리 중 랜덤 선택
        article_types = [
            ArticleType.GENERAL,      # 실시간
            ArticleType.REVIEW,       # 리뷰
            ArticleType.LOVE_CONCERNS # 연애상담
        ]
        return random.choice(article_types)
    

    
    def get_status(self):
        """스케줄러 상태 반환"""
        jobs = self.scheduler.get_jobs()
        
        next_comment_job = None
        next_post_job = None
        
        for job in jobs:
            if 'auto_comment' in job.id:
                next_comment_job = job
            elif 'auto_post' in job.id:
                next_post_job = job
        
        return {
            "is_running": self.is_running,
            "next_comment_time": next_comment_job.next_run_time if next_comment_job else None,
            "next_post_time": next_post_job.next_run_time if next_post_job else None,
            "total_jobs": len(jobs)
        }

# 전역 스케줄러 서비스 인스턴스
scheduler_service = SchedulerService()
