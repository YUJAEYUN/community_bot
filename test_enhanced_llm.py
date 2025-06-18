#!/usr/bin/env python3
"""
고도화된 LLM 서비스 테스트 스크립트
"""

import asyncio
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.llm_service import llm_service

async def test_sentiment_analysis():
    """감성 분석 테스트"""
    print("=== 감성 분석 테스트 ===")
    
    test_feeds = [
        "오늘 카페에서 공부했는데 분위기가 너무 좋았어요! 추천해드릴게요 😊",
        "매칭이 전혀 안 되네요... 이 앱 진짜 별로인 것 같아요",
        "요즘 과제가 너무 많아서 힘들어요 ㅠㅠ 다들 어떻게 하시나요?",
        "어제 본 영화 정말 재밌었어요! 로맨스 영화 좋아하시는 분들께 추천!",
        "외모가 별로라서 매칭이 안 되는 것 같아요... 너무 우울해요"
    ]
    
    for i, feed in enumerate(test_feeds, 1):
        print(f"\n{i}. 피드: {feed}")
        result = await llm_service.analyze_sentiment(feed)
        print(f"   결과: {'긍정' if result.is_positive else '부정'} (신뢰도: {result.confidence})")
        print(f"   사유: {result.reason}")

async def test_comment_generation():
    """댓글 생성 테스트"""
    print("\n=== 댓글 생성 테스트 ===")
    
    test_feeds = [
        "오늘 처음으로 혼자 영화관에 갔는데 생각보다 괜찮네요!",
        "건대 맛집 추천해주세요! 혼밥하기 좋은 곳으로요",
        "요즘 과제 때문에 스트레스가 너무 심해요... 다들 어떻게 푸시나요?",
        "어제 소개팅 갔는데 분위기가 너무 어색했어요 ㅠㅠ",
        "새로운 취미를 시작하고 싶은데 뭐가 좋을까요?"
    ]
    
    for i, feed in enumerate(test_feeds, 1):
        print(f"\n{i}. 피드: {feed}")
        
        # 감성 분석 먼저
        sentiment = await llm_service.analyze_sentiment(feed)
        if sentiment.is_positive:
            comment = await llm_service.generate_comment(feed)
            print(f"   댓글: {comment}")
        else:
            print(f"   댓글 생성 안함 (부정적 피드)")

async def test_post_generation():
    """게시글 생성 테스트"""
    print("\n=== 게시글 생성 테스트 ===")
    
    article_types = ["general", "review", "love-concerns"]
    
    for article_type in article_types:
        print(f"\n카테고리: {article_type}")
        title, content = await llm_service.generate_post(article_type)
        print(f"제목: {title}")
        print(f"내용: {content}")
        print("-" * 50)

async def main():
    """메인 테스트 함수"""
    print("🤖 고도화된 LLM 서비스 테스트 시작\n")
    
    try:
        await test_sentiment_analysis()
        await test_comment_generation()
        await test_post_generation()
        
        print("\n✅ 모든 테스트 완료!")
        
    except Exception as e:
        print(f"\n❌ 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 환경 변수 확인
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("   .env 파일을 확인하거나 환경 변수를 설정해주세요.")
        sys.exit(1)
    
    asyncio.run(main())
