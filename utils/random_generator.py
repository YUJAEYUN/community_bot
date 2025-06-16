"""
랜덤 닉네임, 대학명, 숫자 조합 생성 유틸리티
"""

import random

# 대학명 리스트
UNIVERSITIES = [
    "서울대", "연세대", "고려대", "성균관대", "한양대", "중앙대", "경희대", "한국외대",
    "서강대", "이화여대", "홍익대", "건국대", "동국대", "숭실대", "세종대", "광운대",
    "국민대", "명지대", "단국대", "인하대", "아주대", "가천대", "한국항공대", "서울시립대",
    "부산대", "경북대", "전남대", "충남대", "전북대", "강원대", "제주대", "충북대"
]

# 닉네임 접두사 리스트
NICKNAME_PREFIXES = [
    "행복한", "밝은", "친절한", "따뜻한", "상냥한", "활발한", "긍정적인", "웃는",
    "즐거운", "사랑스러운", "귀여운", "멋진", "훌륭한", "착한", "성실한", "열정적인",
    "유쾌한", "발랄한", "당당한", "자신감있는", "매력적인", "센스있는", "재미있는", "똑똑한",
    "창의적인", "로맨틱한", "달콤한", "포근한", "신나는", "기운찬", "희망찬", "꿈많은"
]

def generate_random_author_name() -> str:
    """
    랜덤한 작성자명을 생성합니다.
    형식: {닉네임접두사}{대학명} {3~8자리 숫자}
    
    Returns:
        str: 생성된 작성자명 (예: "행복한서울대 12345")
    """
    prefix = random.choice(NICKNAME_PREFIXES)
    university = random.choice(UNIVERSITIES)
    
    # 3~8자리 랜덤 숫자 생성
    num_digits = random.randint(3, 8)
    random_number = random.randint(10**(num_digits-1), 10**num_digits - 1)
    
    return f"{prefix}{university} {random_number}"

def generate_comment_signature(comment: str) -> str:
    """
    댓글에 서명을 추가합니다.
    
    Args:
        comment (str): 원본 댓글
        
    Returns:
        str: 서명이 추가된 댓글
    """
    author_name = generate_random_author_name()
    return f"{comment} - {author_name} 드림"

def generate_post_signature() -> str:
    """
    게시글 작성자 서명을 생성합니다.
    
    Returns:
        str: 게시글 작성자 서명
    """
    author_name = generate_random_author_name()
    return f"- {author_name} 님의 질문"

def get_random_interval_minutes(min_minutes: int, max_hours: int) -> int:
    """
    랜덤한 시간 간격을 분 단위로 반환합니다.
    
    Args:
        min_minutes (int): 최소 분
        max_hours (int): 최대 시간
        
    Returns:
        int: 랜덤 간격 (분)
    """
    max_minutes = max_hours * 60
    return random.randint(min_minutes, max_minutes)
