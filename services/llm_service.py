"""
LangChain을 활용한 고도화된 LLM 서비스
감성 분석, 댓글 생성, 게시글 생성 기능을 제공합니다.
더 자연스럽고 사람같은 응답을 위한 고급 프롬프트 엔지니어링 적용.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Tuple, Optional, List, Dict
import json
import logging
import random
import re

from config import settings
from models.schemas import SentimentAnalysisResult

# 로깅 설정
logger = logging.getLogger(__name__)

# 페르소나 정의
class PersonaConfig(BaseModel):
    """AI 페르소나 설정"""
    personality: str = Field(description="성격 특성")
    tone: str = Field(description="말투")
    interests: List[str] = Field(description="관심사")
    writing_style: str = Field(description="글쓰기 스타일")

# 다양한 페르소나 정의
PERSONAS = [
    PersonaConfig(
        personality="친근하고 활발한",
        tone="밝고 에너지 넘치는 말투, 이모티콘 적극 활용",
        interests=["카페투어", "맛집탐방", "영화감상", "운동"],
        writing_style="짧고 임팩트 있는 문장, 감탄사 많이 사용"
    ),
    PersonaConfig(
        personality="차분하고 따뜻한",
        tone="정중하고 공감적인 말투, 부드러운 표현",
        interests=["독서", "음악감상", "산책", "요리"],
        writing_style="정성스럽고 세심한 표현, 위로의 말 많이 사용"
    ),
    PersonaConfig(
        personality="유머러스하고 재치있는",
        tone="위트 있고 장난스러운 말투, 적절한 농담",
        interests=["게임", "웹툰", "유튜브", "밈문화"],
        writing_style="재미있는 표현과 은어 적절히 사용"
    ),
    PersonaConfig(
        personality="진지하고 신중한",
        tone="차분하고 논리적인 말투, 깊이 있는 조언",
        interests=["스터디", "자기계발", "토론", "시사"],
        writing_style="체계적이고 구체적인 설명"
    ),
    PersonaConfig(
        personality="감성적이고 로맨틱한",
        tone="감성적이고 시적인 표현, 따뜻한 말투",
        interests=["연애", "감성카페", "일몰", "드라마"],
        writing_style="감정이 풍부한 표현, 공감 위주"
    )
]

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
    
    def _get_random_persona(self) -> PersonaConfig:
        """랜덤한 페르소나를 선택합니다."""
        return random.choice(PERSONAS)

    def _analyze_feed_context(self, feed_content: str) -> Dict[str, any]:
        """피드 내용을 분석하여 컨텍스트를 추출합니다."""
        context = {
            "has_question": "?" in feed_content or any(word in feed_content.lower() for word in ["어떻게", "뭐", "어디", "언제", "왜", "누구"]),
            "is_emotional": any(word in feed_content for word in ["ㅠㅠ", "ㅜㅜ", "😭", "😢", "힘들", "우울", "슬프", "기쁘", "행복", "좋아"]),
            "mentions_dating": any(word in feed_content for word in ["연애", "썸", "소개팅", "데이트", "남친", "여친", "애인"]),
            "mentions_food": any(word in feed_content for word in ["맛집", "카페", "음식", "먹", "맛있", "맛없"]),
            "mentions_hobby": any(word in feed_content for word in ["취미", "운동", "영화", "게임", "독서", "음악"]),
            "length": len(feed_content)
        }
        return context

    def _setup_chains(self):
        """LangChain 체인들을 설정합니다."""

        # 고도화된 감성 분석 프롬프트
        self.sentiment_prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 소개팅 앱 커뮤니티의 피드 내용을 정밀하게 분석하는 전문가입니다.
피드의 감정, 의도, 맥락을 종합적으로 고려하여 댓글 생성 적합성을 판단해주세요.

🚫 댓글 생성 금지 (부정적 분류):
- 매칭/만남 실패에 대한 강한 불만이나 절망감
- 외모, 스펙 비하나 차별적 표현
- 서비스/앱에 대한 강한 비판이나 욕설
- 극도로 우울하거나 자해 암시하는 내용
- 타인을 비난하거나 공격하는 내용
- 성적이거나 부적절한 내용
- 스팸성 홍보나 광고성 내용

✅ 댓글 생성 적합 (긍정적 분류):
- 일상적인 이야기나 경험 공유
- 연애/만남에 대한 건전한 고민이나 질문
- 취미, 관심사, 학교생활 관련 이야기
- 맛집, 카페, 데이트 장소 후기
- 가벼운 TMI나 일상 공유
- 조언이나 의견을 구하는 질문
- 긍정적인 경험담이나 후기

판단 기준:
1. 전체적인 톤과 감정 (70%)
2. 구체적인 키워드와 표현 (20%)
3. 커뮤니티 분위기에 미칠 영향 (10%)

응답은 반드시 다음 JSON 형식으로만 해주세요:
{{
    "is_positive": true,
    "confidence": 0.9,
    "reason": "판단 근거",
    "emotion": "감지된 주요 감정",
    "topic": "주요 주제"
}}"""),
            ("human", "분석할 피드 내용: {feed_content}")
        ])

        self.sentiment_chain = self.sentiment_prompt | self.llm

        # 페르소나 기반 댓글 생성 프롬프트 템플릿
        self.comment_prompt_template = """당신은 {personality} 20대 대학생입니다.
소개팅 앱 커뮤니티에서 다른 사용자의 피드에 자연스럽고 진심어린 댓글을 작성해주세요.

🎭 당신의 캐릭터:
- 성격: {personality}
- 말투: {tone}
- 관심사: {interests}
- 글쓰기 스타일: {writing_style}

📝 댓글 작성 원칙:
1. 실제 대학생이 쓸 법한 자연스러운 표현 사용
2. 피드 내용에 구체적으로 반응하기
3. 과도한 칭찬보다는 진솔한 공감 표현
4. 적절한 이모티콘 사용 (0-2개)
5. 길이: 1-3문장 (너무 길지 않게)

💡 상황별 댓글 스타일:
- 질문 피드 → 경험 공유나 의견 제시
- 고민 피드 → 공감과 격려
- 후기 피드 → 관심 표현이나 추가 질문
- 일상 피드 → 가벼운 반응이나 공감

🚫 피해야 할 표현:
- 너무 완벽하거나 모범적인 답변
- 과도한 격려나 응원
- 뻔한 위로의 말
- 상투적인 표현

실제 대학생처럼 자연스럽고 진짜 같은 댓글을 작성해주세요."""

        # 고도화된 게시글 생성 프롬프트 템플릿
        self.post_prompt_template = """당신은 {personality} 20대 대학생입니다.
소개팅 앱 커뮤니티에 자연스럽고 매력적인 게시글을 작성해주세요.

🎭 당신의 캐릭터:
- 성격: {personality}
- 말투: {tone}
- 관심사: {interests}
- 글쓰기 스타일: {writing_style}

📝 게시글 작성 가이드:

**{topic_category}** 카테고리 특화:
{topic_guide}

✨ 자연스러운 게시글 작성법:
1. 제목: 8-15자, 궁금증을 유발하는 자연스러운 표현
2. 내용: 2-4문장, 실제 경험담처럼 구체적으로
3. 말투: 반말 기본, 존댓말 가끔 섞어서 자연스럽게
4. 이모지: 1-3개 적절히 사용
5. 마무리: 댓글 유도하는 질문이나 의견 요청

🎯 실제 대학생 특징 반영:
- 약간의 줄임말이나 신조어 자연스럽게 사용
- 완벽하지 않은 문장 구조도 OK
- 솔직하고 진솔한 톤
- 과도한 정중함보다는 친근함
- 구체적인 상황이나 경험 언급

💡 카테고리별 팁:
- 실시간: 지금 당장의 고민이나 궁금증
- 리뷰: 구체적인 장소명과 솔직한 후기
- 연애상담: 현실적이고 공감 가능한 상황

응답은 반드시 다음 JSON 형식으로만 해주세요:
{{
    "title": "게시글 제목",
    "content": "게시글 내용"
}}"""
    
    async def analyze_sentiment(self, feed_content: str) -> SentimentAnalysisResult:
        """
        고도화된 감성 분석을 수행합니다.

        Args:
            feed_content (str): 분석할 피드 내용

        Returns:
            SentimentAnalysisResult: 감성 분석 결과
        """
        try:
            result = await self.sentiment_chain.ainvoke({"feed_content": feed_content})

            # JSON 파싱
            content = result.content.strip()
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]

            parsed_result = json.loads(content)

            # 추가 정보도 포함하여 반환
            sentiment_result = SentimentAnalysisResult(
                is_positive=parsed_result["is_positive"],
                confidence=parsed_result["confidence"],
                reason=parsed_result["reason"]
            )

            # 로깅으로 분석 결과 기록
            logger.info(f"감성 분석 완료 - 긍정: {sentiment_result.is_positive}, "
                       f"신뢰도: {sentiment_result.confidence}, "
                       f"감정: {parsed_result.get('emotion', 'N/A')}, "
                       f"주제: {parsed_result.get('topic', 'N/A')}")

            return sentiment_result

        except Exception as e:
            logger.error(f"감성 분석 중 오류 발생: {str(e)}")
            # 오류 발생 시 안전하게 부정적으로 분류
            return SentimentAnalysisResult(
                is_positive=False,
                confidence=0.0,
                reason=f"분석 중 오류 발생: {str(e)}"
            )
    
    async def generate_comment(self, feed_content: str) -> str:
        """
        페르소나 기반으로 자연스러운 댓글을 생성합니다.

        Args:
            feed_content (str): 댓글을 달 피드 내용

        Returns:
            str: 생성된 댓글
        """
        try:
            # 랜덤 페르소나 선택
            persona = self._get_random_persona()

            # 피드 컨텍스트 분석
            context = self._analyze_feed_context(feed_content)

            # 페르소나 기반 프롬프트 생성
            comment_prompt = ChatPromptTemplate.from_messages([
                ("system", self.comment_prompt_template.format(
                    personality=persona.personality,
                    tone=persona.tone,
                    interests=", ".join(persona.interests),
                    writing_style=persona.writing_style
                )),
                ("human", f"""피드 내용: {feed_content}

컨텍스트 정보:
- 질문 포함: {context['has_question']}
- 감정적 표현: {context['is_emotional']}
- 연애 관련: {context['mentions_dating']}
- 음식 관련: {context['mentions_food']}
- 취미 관련: {context['mentions_hobby']}

위 정보를 참고하여 자연스럽고 진심어린 댓글을 작성해주세요.""")
            ])

            comment_chain = comment_prompt | self.llm
            result = await comment_chain.ainvoke({})

            # 댓글 품질 검증
            comment = self._validate_and_clean_comment(result.content)

            logger.info(f"댓글 생성 완료 - 페르소나: {persona.personality}, 길이: {len(comment)}")
            return comment

        except Exception as e:
            logger.error(f"댓글 생성 중 오류 발생: {str(e)}")
            # 기본 댓글 반환
            return self._get_fallback_comment(feed_content)

    def _validate_and_clean_comment(self, comment: str) -> str:
        """댓글 품질을 검증하고 정리합니다."""
        # 기본 정리
        comment = comment.strip()

        # 따옴표 제거
        if comment.startswith('"') and comment.endswith('"'):
            comment = comment[1:-1]

        # 너무 긴 댓글 줄이기 (150자 제한)
        if len(comment) > 150:
            sentences = comment.split('.')
            comment = sentences[0] + ('.' if len(sentences) > 1 else '')

        # 부적절한 표현 필터링
        inappropriate_words = ["죽", "자살", "욕설", "비하"]
        for word in inappropriate_words:
            if word in comment:
                return "공감해요! 좋은 하루 되세요 😊"

        return comment

    def _get_fallback_comment(self, feed_content: str = None) -> str:
        """오류 시 사용할 기본 댓글을 반환합니다."""
        fallback_comments = [
            "공감해요! 😊",
            "좋은 글이네요!",
            "저도 비슷한 생각이에요",
            "흥미로운 이야기네요!",
            "좋은 하루 되세요 ✨"
        ]
        return random.choice(fallback_comments)
    
    async def generate_post(self, article_type: Optional[str] = None) -> Tuple[str, str]:
        """
        페르소나 기반으로 자연스러운 게시글을 생성합니다.

        Args:
            article_type (Optional[str]): 게시글 타입 ('general', 'review', 'love-concerns')

        Returns:
            Tuple[str, str]: (제목, 내용)
        """
        try:
            # 랜덤 페르소나 선택
            persona = self._get_random_persona()

            # 카테고리별 상세 가이드 설정
            category_guides = {
                "general": {
                    "category": "실시간",
                    "guide": """- 지금 당장의 고민이나 궁금증 (과제, 시험, 일상)
- 학교생활 TMI나 에피소드
- 요즘 트렌드나 관심사
- 가벼운 질문이나 의견 요청
예시: "중간고사 망한 사람 나만 아니겠지?", "요즘 넷플릭스 뭐 봐요?", "혼밥 맛집 추천해주세요"""
                },
                "review": {
                    "category": "리뷰",
                    "guide": """- 실제 다녀온 장소의 솔직한 후기
- 구체적인 장소명과 경험담
- 맛집, 카페, 데이트 장소, 영화, 드라마 등
- 별점이나 추천 여부 포함
예시: "홍대 ○○카페 분위기 미쳤다", "어제 본 ○○ 영화 후기", "건대 데이트 코스 추천"""
                },
                "love-concerns": {
                    "category": "연애상담",
                    "guide": """- 현실적이고 공감 가능한 연애 상황
- 썸, 소개팅, 연애 고민
- 구체적인 상황 설명과 조언 요청
- 연락 빈도, 데이트 관련 고민
예시: "썸남이 갑자기 연락이 뜸해졌어요", "소개팅 옷차림 조언 구해요", "고백 타이밍 언제가 좋을까요?"""
                }
            }

            # 기본값 설정
            if article_type not in category_guides:
                article_type = random.choice(list(category_guides.keys()))

            guide_info = category_guides[article_type]

            # 페르소나 기반 프롬프트 생성
            post_prompt = ChatPromptTemplate.from_messages([
                ("system", self.post_prompt_template.format(
                    personality=persona.personality,
                    tone=persona.tone,
                    interests=", ".join(persona.interests),
                    writing_style=persona.writing_style,
                    topic_category=guide_info["category"],
                    topic_guide=guide_info["guide"]
                )),
                ("human", f"{guide_info['category']} 카테고리에 맞는 자연스러운 게시글을 작성해주세요.")
            ])

            post_chain = post_prompt | self.llm
            result = await post_chain.ainvoke({})

            # JSON 파싱 및 검증
            title, content = self._parse_and_validate_post(result.content)

            logger.info(f"게시글 생성 완료 - 카테고리: {article_type}, 페르소나: {persona.personality}")
            logger.info(f"제목: {title}, 내용 길이: {len(content)}")

            return title, content

        except Exception as e:
            logger.error(f"게시글 생성 중 오류 발생: {str(e)}")
            return self._get_fallback_post(article_type)

    def _parse_and_validate_post(self, raw_content: str) -> Tuple[str, str]:
        """게시글 JSON을 파싱하고 검증합니다."""
        try:
            # JSON 파싱
            content = raw_content.strip()
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]

            parsed_result = json.loads(content)
            title = parsed_result.get("title", "").strip()
            post_content = parsed_result.get("content", "").strip()

            # 제목 검증 및 정리
            if not title or len(title) > 50:
                title = "커뮤니티 질문"

            # 내용 검증 및 정리
            if not post_content or len(post_content) > 500:
                post_content = "안녕하세요! 오늘 하루 어떻게 보내셨나요? 😊"

            return title, post_content

        except Exception as e:
            logger.error(f"게시글 파싱 실패: {str(e)}")
            # 정규식으로 추출 시도
            title_match = re.search(r'"title":\s*"([^"]+)"', raw_content)
            content_match = re.search(r'"content":\s*"([^"]+)"', raw_content)

            if title_match and content_match:
                return title_match.group(1), content_match.group(1)

            return "커뮤니티 질문", "안녕하세요! 오늘 하루 어떻게 보내셨나요? 😊"

    def _get_fallback_post(self, article_type: Optional[str]) -> Tuple[str, str]:
        """오류 시 사용할 기본 게시글을 반환합니다."""
        fallback_posts = {
            "general": ("오늘 뭐하셨나요?", "다들 오늘 하루 어떻게 보내셨어요? 저는 과제하다가 포기했네요 ㅠㅠ"),
            "review": ("맛집 추천해주세요", "요즘 괜찮은 맛집이나 카페 있으면 추천해주세요! 혼자 가기 좋은 곳으로요 😊"),
            "love-concerns": ("연애 고민이에요", "요즘 연애가 너무 어려운 것 같아요... 다들 어떻게 생각하세요?")
        }

        return fallback_posts.get(article_type, fallback_posts["general"])

# 전역 LLM 서비스 인스턴스
llm_service = LLMService()
