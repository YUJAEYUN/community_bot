"""
외부 소개팅 서비스 API 연동 서비스
댓글 작성, 게시글 작성 API 호출을 담당합니다.
"""

import httpx
import logging
from typing import Optional, Dict, Any, List
from enum import Enum

from config import settings

# 로깅 설정
logger = logging.getLogger(__name__)

class ArticleType(str, Enum):
    """게시글 타입 열거형 (소개팅 서비스 백엔드와 일치)"""
    GENERAL = "general"        # 실시간 (일반)
    REVIEW = "review"          # 리뷰
    LOVE_CONCERNS = "love-concerns"  # 연애상담

class ExternalAPIService:
    """외부 API 연동 서비스 클래스"""
    
    def __init__(self):
        """외부 API 서비스 초기화"""
        self.base_url = settings.EXTERNAL_API_BASE_URL
        self.token = settings.EXTERNAL_API_TOKEN
        self.dev_mode = settings.DEV_MODE
        self.dev_user_id = settings.DEV_USER_ID

        # HTTP 클라이언트 설정
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}" if self.token else ""
        }

    async def get_article_categories(self) -> Optional[List[Dict]]:
        """게시글 카테고리 목록을 조회합니다."""
        if self.dev_mode:
            logger.info("[개발모드] 카테고리 목록 조회 시뮬레이션")
            return [
                {"code": "general", "name": "일반"},
                {"code": "review", "name": "후기"},
                {"code": "love-concerns", "name": "연애고민"},
                {"code": "hot", "name": "인기"}
            ]

        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/articles/category/list"

                response = await client.get(
                    url,
                    headers=self.headers,
                    timeout=10.0
                )

                if response.status_code == 200:
                    categories = response.json()
                    logger.info(f"카테고리 목록 조회 성공: {len(categories)}개")
                    return categories
                else:
                    logger.error(f"카테고리 목록 조회 실패: {response.status_code} - {response.text}")
                    return None

        except Exception as e:
            logger.error(f"카테고리 목록 조회 중 오류 발생: {str(e)}")
            return None

    async def get_recent_articles(self, category: str = "general", limit: int = 10) -> Optional[list]:
        """
        최근 게시글 목록을 가져옵니다.

        Args:
            category (str): 게시글 카테고리 ('general', 'review', 'love-concerns', 'hot')
            limit (int): 가져올 게시글 수

        Returns:
            Optional[list]: 게시글 목록 또는 None
        """
        if self.dev_mode:
            logger.info(f"[개발모드] 게시글 목록 조회 시뮬레이션 - 카테고리: {category}")
            return [
                {
                    "id": f"dev_article_1_{category}",
                    "title": "개발모드 테스트 게시글 1",
                    "content": "이것은 개발모드에서 생성된 테스트 게시글입니다.",
                    "author": {"name": "테스트유저1"},
                    "createdAt": "2025-06-16T12:00:00Z"
                },
                {
                    "id": f"dev_article_2_{category}",
                    "title": "개발모드 테스트 게시글 2",
                    "content": "두 번째 테스트 게시글입니다.",
                    "author": {"name": "테스트유저2"},
                    "createdAt": "2025-06-16T11:30:00Z"
                }
            ]

        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/articles/{category}"
                params = {"page": 1, "limit": limit}

                response = await client.get(
                    url,
                    params=params,
                    headers=self.headers,
                    timeout=10.0
                )

                if response.status_code == 200:
                    data = response.json()
                    # 응답 구조에 따라 데이터 추출 (items 또는 articles 키 확인)
                    articles = data.get('items', data.get('articles', []))
                    logger.info(f"게시글 목록 조회 성공: {len(articles)}개")
                    return articles
                else:
                    logger.error(f"게시글 목록 조회 실패: {response.status_code} - {response.text}")
                    return None

        except Exception as e:
            logger.error(f"게시글 목록 조회 중 오류 발생: {str(e)}")
            return None
    
    async def create_comment(self, article_id: str, content: str, anonymous: bool = True) -> Optional[Dict[str, Any]]:
        """
        특정 게시글에 댓글을 작성합니다.
        
        Args:
            article_id (str): 게시글 ID
            content (str): 댓글 내용
            anonymous (bool): 익명 처리 여부
            
        Returns:
            Optional[Dict[str, Any]]: 생성된 댓글 정보 또는 None
        """
        if self.dev_mode:
            logger.info(f"[개발모드] 댓글 작성 시뮬레이션 - 게시글 ID: {article_id}, 내용: {content}")
            return {
                "id": f"dev_comment_{article_id}",
                "content": content,
                "anonymous": "AI봇" if anonymous else None,
                "created_at": "2025-06-16T12:00:00Z"
            }
        
        try:
            async with httpx.AsyncClient() as client:
                # AI 전용 댓글 생성 엔드포인트 사용 (매번 다른 닉네임 생성)
                url = f"{self.base_url}/ai/content/articles/{article_id}/comments"

                payload = {
                    "content": content,
                    "anonymous": anonymous
                }

                response = await client.post(
                    url,
                    json=payload,
                    headers=self.headers,
                    timeout=10.0
                )
                
                if response.status_code == 201:
                    result = response.json()
                    logger.info(f"댓글 작성 성공: {result.get('id')}")
                    return result
                else:
                    logger.error(f"댓글 작성 실패: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            logger.error(f"댓글 작성 중 오류 발생: {str(e)}")
            return None
    
    async def create_article(self, title: str, content: str, article_type: ArticleType = ArticleType.GENERAL, anonymous: bool = True) -> Optional[Dict[str, Any]]:
        """
        새로운 게시글을 작성합니다.

        Args:
            title (str): 게시글 제목
            content (str): 게시글 내용
            article_type (ArticleType): 게시글 타입
            anonymous (bool): 익명 처리 여부

        Returns:
            Optional[Dict[str, Any]]: 생성된 게시글 정보 또는 None
        """
        if self.dev_mode:
            logger.info(f"[개발모드] 게시글 작성 시뮬레이션 - 제목: {title}, 타입: {article_type}")
            return {
                "id": f"dev_article_{hash(title)}",
                "title": title,
                "content": content,
                "type": article_type.value,
                "anonymous": "AI봇" if anonymous else None,
                "created_at": "2025-06-16T12:00:00Z"
            }

        try:
            async with httpx.AsyncClient() as client:
                # AI 전용 게시글 생성 엔드포인트 사용 (매번 다른 닉네임 생성)
                url = f"{self.base_url}/ai/content/articles"

                # AI 전용 API 스펙에 맞는 payload
                payload = {
                    "title": title,
                    "content": content,
                    "type": article_type.value,  # 'general', 'review', 'love-concerns'
                    "anonymous": anonymous
                }

                response = await client.post(
                    url,
                    json=payload,
                    headers=self.headers,
                    timeout=10.0
                )

                if response.status_code == 201:
                    # 응답이 비어있을 수 있으므로 안전하게 처리
                    try:
                        if response.text.strip():
                            result = response.json()
                            logger.info(f"게시글 작성 성공: {result.get('id', 'ID 없음')}")
                            return result
                        else:
                            # 응답이 비어있지만 성공한 경우
                            logger.info("게시글 작성 성공 (응답 본문 없음)")
                            return {"success": True, "message": "게시글이 성공적으로 생성되었습니다"}
                    except Exception as json_error:
                        logger.warning(f"응답 JSON 파싱 실패, 하지만 게시글 생성은 성공: {json_error}")
                        return {"success": True, "message": "게시글이 성공적으로 생성되었습니다"}
                else:
                    logger.error(f"게시글 작성 실패: {response.status_code} - {response.text}")
                    return None

        except Exception as e:
            logger.error(f"게시글 작성 중 오류 발생: {str(e)}")
            return None
    
    async def get_article_details(self, article_id: str) -> Optional[Dict[str, Any]]:
        """
        특정 게시글의 상세 정보를 가져옵니다.
        
        Args:
            article_id (str): 게시글 ID
            
        Returns:
            Optional[Dict[str, Any]]: 게시글 상세 정보 또는 None
        """
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/articles/details/{article_id}"
                
                response = await client.get(
                    url,
                    headers=self.headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"게시글 상세 조회 성공: {article_id}")
                    return result
                else:
                    logger.error(f"게시글 상세 조회 실패: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            logger.error(f"게시글 상세 조회 중 오류 발생: {str(e)}")
            return None

# 전역 외부 API 서비스 인스턴스
external_api_service = ExternalAPIService()
