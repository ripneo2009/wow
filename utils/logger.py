"""
로깅 유틸리티 모듈
- 콘솔 및 파일 로깅 설정
"""
import logging
import os
import sys
from datetime import datetime
from config import LOGS_DIR

def setup_logger(name="app_logger"):
    """
    로거 설정 및 반환
    
    Args:
        name: 로거 이름
        
    Returns:
        logger: 설정된 로거 인스턴스
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 이미 핸들러가 있다면 추가하지 않음 (중복 로그 방지)
    if logger.handlers:
        return logger
    
    # 포맷 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 파일 핸들러 (날짜별 로그 파일)
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(LOGS_DIR, f"app_{today}.log")
    
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"로그 파일 생성 실패: {e}")
        
    return logger
