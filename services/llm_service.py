"""
LangChain을 활용한 LLM 서비스
감성 분석, 댓글 생성, 게시글 생성 기능을 제공합니다.
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from typing import Tuple, Optional
import json
import logging

from config import settings
from models.schemas import SentimentAnalysisResult

# 로깅 설정
logger = logging.getLogger(__name__)

class LLMService:
    """LLM 서비스 클래스"""
    
    def __init__(self):
        """LLM 서비스 초기화"""
        self.llm = self._initialize_llm()
        self._setup_chains()
    
    def _initialize_llm(self):
        """LLM 모델 초기화"""
        if settings.DEFAULT_LLM_PROVIDER == "openai":
            return ChatOpenAI(
                openai_api_key=settings.OPENAI_API_KEY,
                model_name=settings.OPENAI_MODEL,
                temperature=0.7
            )
        else:
            # Google Gemini 설정 (추후 구현)
            raise NotImplementedError("Google Gemini 연동은 추후 구현 예정입니다.")
    
    def _setup_chains(self):
        """LangChain 체인들을 설정합니다."""

        # 감성 분석 프롬프트
        self.sentiment_prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 소개팅 앱 커뮤니티의 피드 내용을 분석하는 전문가입니다.
주어진 피드가 긍정적인지 부정적인지 판단해주세요.

다음과 같은 내용은 부정적으로 분류해야 합니다:
- 매칭이 안 된다는 불만
- 외모 비하나 차별적 표현
- 서비스에 대한 강한 불만이나 비판
- 극도로 우울하거나 절망적인 내용
- 타인을 비난하거나 공격하는 내용

긍정적인 내용:
- 일상적인 이야기나 경험 공유
- 연애나 만남에 대한 희망적인 내용
- 취미나 관심사에 대한 이야기
- 질문이나 조언 요청

응답은 반드시 다음 JSON 형식으로만 해주세요:
{{
    "is_positive": true,
    "confidence": 0.9,
    "reason": "판단 근거"
}}"""),
            ("human", "분석할 피드 내용: {feed_content}")
        ])

        self.sentiment_chain = self.sentiment_prompt | self.llm
        
        # 댓글 생성 프롬프트
        self.comment_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
            당신은 소개팅 앱 커뮤니티에서 활동하는 친근하고 긍정적인 사용자입니다.
            주어진 피드에 대해 공감하고 격려하는 댓글을 작성해주세요.

            댓글 작성 가이드라인:
            - 따뜻하고 친근한 톤으로 작성
            - 피드 작성자를 격려하고 응원하는 내용
            - 2-3문장 정도의 적당한 길이
            - 이모티콘 사용 가능 (과도하지 않게)
            - 구체적인 조언보다는 공감과 격려 위주

            예시:
            - "정말 공감돼요! 저도 비슷한 경험이 있어서 마음이 이해가 가네요 😊"
            - "힘내세요! 좋은 일이 곧 생길 거예요 ✨"
            - "와 정말 멋진 취미네요! 저도 관심이 생겼어요"
            """),
            HumanMessage(content="댓글을 달 피드 내용: {feed_content}")
        ])

        self.comment_chain = self.comment_prompt | self.llm
        
        # 게시글 생성 프롬프트 (실제 대학생 스타일로 특화)
        self.post_prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 20대 대학생이 되어 소개팅 앱 커뮤니티에 자연스러운 게시글을 작성합니다.
실제 대학생들이 쓸 법한 진짜 같은 게시글을 만들어주세요.

카테고리별 특화 가이드:

**실시간 - 대학생 일상 TMI, 고민, 궁금한 것들, 학교생활, 취미, 트렌드**:
- 일상 TMI, 고민, 궁금한 것들
- 학교생활, 취미, 트렌드 관련
- 예시: "과제 미루는 습관 어떻게 고치지", "요즘 인기 있는 게임 뭐예요?", "혼자 영화관 가는 거 어때요?"

**리뷰 - 실제 다녀온 데이트 장소, 맛집, 카페, 영화, 드라마 후기**:
- 실제 다녀온 곳 후기 (구체적 장소명 포함)
- 솔직한 경험담과 평가
- 예시: "건대 ○○카페 분위기 진짜 좋네요", "어제 본 ○○ 영화 완전 꿀잼", "신촌 ○○ 맛집 인정합니다"

**연애상담 - 썸 상황, 연애 고민, 소개팅 준비, 연락 빈도 등 현실적인 연애 상황**:
- 진짜 고민 같은 상황 설정
- 구체적이고 현실적인 연애 상황
- 예시: "3개월째 썸인데 고백해도 될까요", "소개팅에서 뭘 입어야 할지 모르겠어요", "연락 빈도 어느 정도가 적당한가요?"

작성 스타일:
- 제목: 10-15자, 자연스럽고 클릭하고 싶게
- 내용: 실제 대학생이 쓴 것처럼 자연스럽게 2-3문장
- 반말 사용, 이모지 1-2개 적절히
- 댓글 유도하는 질문으로 마무리
- 너무 완벽하지 않게, 약간의 오타나 줄임말도 자연스럽게

응답은 반드시 다음 JSON 형식으로만 해주세요:
{{
    "title": "게시글 제목",
    "content": "게시글 내용"
}}"""),
            ("human", "다음 주제로 게시글을 작성해주세요: {topic}")
        ])

        self.post_chain = self.post_prompt | self.llm
    
    async def analyze_sentiment(self, feed_content: str) -> SentimentAnalysisResult:
        """
        피드 내용의 감성을 분석합니다.

        Args:
            feed_content (str): 분석할 피드 내용

        Returns:
            SentimentAnalysisResult: 감성 분석 결과
        """
        try:
            result = await self.sentiment_chain.ainvoke({"feed_content": feed_content})

            # JSON 파싱
            parsed_result = json.loads(result.content)

            return SentimentAnalysisResult(
                is_positive=parsed_result["is_positive"],
                confidence=parsed_result["confidence"],
                reason=parsed_result["reason"]
            )
        except Exception as e:
            # 오류 발생 시 안전하게 부정적으로 분류
            return SentimentAnalysisResult(
                is_positive=False,
                confidence=0.0,
                reason=f"분석 중 오류 발생: {str(e)}"
            )
    
    async def generate_comment(self, feed_content: str) -> str:
        """
        피드에 대한 댓글을 생성합니다.

        Args:
            feed_content (str): 댓글을 달 피드 내용

        Returns:
            str: 생성된 댓글
        """
        result = await self.comment_chain.ainvoke({"feed_content": feed_content})
        return result.content
    
    async def generate_post(self, article_type: Optional[str] = None) -> Tuple[str, str]:
        """
        카테고리별 맞춤 게시글을 생성합니다.

        Args:
            article_type (Optional[str]): 게시글 타입 ('general', 'review', 'love-concerns')

        Returns:
            Tuple[str, str]: (제목, 내용)
        """
        # 카테고리별 구체적인 주제 설정
        topic_map = {
            "general": "실시간 - 대학생 일상 TMI, 고민, 궁금한 것들, 학교생활, 취미, 트렌드",
            "review": "리뷰 - 실제 다녀온 데이트 장소, 맛집, 카페, 영화, 드라마 후기",
            "love-concerns": "연애상담 - 썸 상황, 연애 고민, 소개팅 준비, 연락 빈도 등 현실적인 연애 상황"
        }

        topic = topic_map.get(article_type, "대학생들의 자유로운 주제")
        result = await self.post_chain.ainvoke({"topic": topic})

        try:
            # JSON 파싱 시도
            content = result.content.strip()

            # 혹시 마크다운 코드 블록으로 감싸져 있다면 제거
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]

            content = content.strip()

            parsed_result = json.loads(content)
            title = parsed_result.get("title", "커뮤니티 질문")
            post_content = parsed_result.get("content", "내용을 생성하지 못했습니다.")

            logger.info(f"게시글 생성 성공 - 제목: {title}")
            logger.info(f"게시글 생성 성공 - 내용: {post_content[:50]}...")

            return title, post_content

        except Exception as e:
            # JSON 파싱 실패 시 로그 출력 및 기본값 반환
            logger.error(f"JSON 파싱 실패: {str(e)}")
            logger.error(f"원본 응답: {result.content}")

            # 원본 응답에서 제목과 내용을 추출 시도
            content = result.content
            if '"title"' in content and '"content"' in content:
                # 간단한 정규식으로 제목과 내용 추출 시도
                import re
                title_match = re.search(r'"title":\s*"([^"]+)"', content)
                content_match = re.search(r'"content":\s*"([^"]+)"', content)

                if title_match and content_match:
                    return title_match.group(1), content_match.group(1)

            return "커뮤니티 질문", "안녕하세요! 오늘 하루 어떻게 보내셨나요? 😊"

# 전역 LLM 서비스 인스턴스
llm_service = LLMService()
