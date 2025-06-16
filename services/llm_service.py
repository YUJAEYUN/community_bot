"""
LangChain을 활용한 LLM 서비스
감성 분석, 댓글 생성, 게시글 생성 기능을 제공합니다.
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from typing import Tuple, Optional
import json

from config import settings
from models.schemas import SentimentAnalysisResult

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
            SystemMessage(content="""
            당신은 소개팅 앱 커뮤니티의 피드 내용을 분석하는 전문가입니다.
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

            응답은 다음 JSON 형식으로 해주세요:
            {
                "is_positive": true/false,
                "confidence": 0.0-1.0,
                "reason": "판단 근거"
            }
            """),
            HumanMessage(content="분석할 피드 내용: {feed_content}")
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
        
        # 게시글 생성 프롬프트
        self.post_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
            당신은 소개팅 앱 커뮤니티를 활성화시키는 역할을 합니다.
            사용자들이 관심을 가지고 참여할 만한 가벼운 질문이나 흥미로운 주제의 게시글을 작성해주세요.

            게시글 주제:
            - 연애와 관련된 가벼운 질문
            - 일상생활 경험 공유
            - 취미나 관심사에 대한 이야기
            - 계절이나 시기에 맞는 주제
            - MBTI, 혈액형 등 재미있는 성격 테스트

            형식:
            제목: 간단하고 흥미로운 제목
            내용: 2-4문장 정도의 본문과 질문

            응답은 다음 JSON 형식으로 해주세요:
            {
                "title": "게시글 제목",
                "content": "게시글 내용"
            }
            """),
            HumanMessage(content="주제 (선택사항): {topic}")
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
    
    async def generate_post(self, topic: Optional[str] = None) -> Tuple[str, str]:
        """
        게시글을 생성합니다.

        Args:
            topic (Optional[str]): 게시글 주제 (선택사항)

        Returns:
            Tuple[str, str]: (제목, 내용)
        """
        result = await self.post_chain.ainvoke({"topic": topic or "자유 주제"})

        try:
            parsed_result = json.loads(result.content)
            return parsed_result["title"], parsed_result["content"]
        except:
            # JSON 파싱 실패 시 기본값 반환
            return "커뮤니티 질문", result.content

# 전역 LLM 서비스 인스턴스
llm_service = LLMService()
