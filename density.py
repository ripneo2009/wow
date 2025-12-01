"""
혼잡도 지수(CDI: Crowd Density Index) 계산 모듈
- 전체 인원수와 고밀집 구역을 기반으로 위험도 계산
"""

import numpy as np


def calculate_cdi(total_people, frame_area, grid_counts, high_density_threshold=3, weight=0.3):
    """
    혼잡도 지수(CDI) 계산
    
    공식: (전체 인원수 / 화면 면적) + (고밀집 구역 개수 × 가중치)
    결과를 0~1 사이 값으로 정규화
    
    Args:
        total_people: 전체 검출된 사람 수
        frame_area: 프레임 면적 (픽셀 단위)
        grid_counts: 각 그리드 구역의 사람 수 리스트
        high_density_threshold: 고밀집 구역 판단 임계값 (기본값: 3명)
        weight: 고밀집 구역 가중치 (기본값: 0.3)
    
    Returns:
        cdi: 혼잡도 지수 (0.0 ~ 1.0)
    """
    # 면적당 인원 밀도 계산 (정규화를 위해 10000으로 나눔)
    density = (total_people / frame_area) * 10000 if frame_area > 0 else 0
    
    # 고밀집 구역 개수 계산
    high_density_zones = sum(1 for count in grid_counts if count >= high_density_threshold)
    
    # CDI 계산
    cdi = density + (high_density_zones * weight)
    
    # 0~1 사이로 정규화 (최대값을 100으로 가정하고 클리핑)
    cdi = min(cdi / 100.0, 1.0)
    cdi = max(cdi, 0.0)
    
    return cdi


def get_risk_level(cdi):
    """
    혼잡도 지수에 따른 위험도 레벨 반환
    
    Args:
        cdi: 혼잡도 지수 (0.0 ~ 1.0)
    
    Returns:
        risk_level: 위험도 레벨 ("GREEN", "YELLOW", "ORANGE", "RED")
        risk_color: 위험도 색상 코드 (RGB 튜플)
        risk_label: 위험도 라벨 (한글)
    """
    if cdi < 0.3:
        return "GREEN", (0, 255, 0), "안전"
    elif cdi < 0.6:
        return "YELLOW", (255, 255, 0), "주의"
    elif cdi < 0.8:
        return "ORANGE", (255, 165, 0), "경고"
    else:
        return "RED", (255, 0, 0), "위험"


def get_risk_level_info(cdi):
    """
    위험도 레벨 정보를 딕셔너리로 반환
    
    Args:
        cdi: 혼잡도 지수
    
    Returns:
        dict: 위험도 정보 딕셔너리
    """
    risk_level, risk_color, risk_label = get_risk_level(cdi)
    
    return {
        "level": risk_level,
        "color": risk_color,
        "label": risk_label,
        "cdi": cdi,
        "cdi_percent": cdi * 100
    }

