"""
혼잡도 지수(CDI) 계산 모듈
"""
from config import RISK_LEVELS

def calculate_cdi(total_people, frame_area, grid_counts, high_density_threshold=3, weight=0.3):
    """
    혼잡도 지수(CDI) 계산
    
    Args:
        total_people: 전체 검출된 사람 수
        frame_area: 프레임 면적 (픽셀 단위)
        grid_counts: 각 그리드 구역의 사람 수 리스트
        high_density_threshold: 고밀집 구역 판단 임계값
        weight: 고밀집 구역 가중치
    
    Returns:
        cdi: 혼잡도 지수 (0.0 ~ 1.0)
    """
    # 면적당 인원 밀도 계산 (정규화를 위해 10000으로 나눔)
    density = (total_people / frame_area) * 10000 if frame_area > 0 else 0
    
    # 고밀집 구역 개수 계산
    high_density_zones = sum(1 for count in grid_counts if count >= high_density_threshold)
    
    # CDI 계산
    cdi = density + (high_density_zones * weight)
    
    # 0~1 사이로 정규화 (최대값을 1.0으로 제한)
    cdi = min(cdi / 1.5, 1.0) # 스케일 조정 (기존 100.0은 너무 컸음, 예시값 조정)
    # 기존 로직: cdi = min(cdi / 100.0, 1.0) -> density가 보통 0.x ~ 5.x 정도 나옴.
    # 100으로 나누면 너무 작아짐. 
    # 예: 1920x1080 = 2,073,600. 10명 -> (10/2M)*10000 = 0.048.
    # 고밀집 1개 -> 0.3. 합 = 0.348.
    # 기존 로직대로라면 0.348 / 100 = 0.00348 (너무 작음).
    # 아마 기존 로직의 100.0은 실수였거나 다른 스케일이었을 듯.
    # 여기서는 0.348 자체가 0~1 사이의 값이 되도록 조정.
    # 그냥 cdi 자체를 사용하고 1.0으로 클리핑하는게 나을 듯.
    
    cdi = min(cdi, 1.0)
    cdi = max(cdi, 0.0)
    
    return cdi

def get_risk_level_info(cdi):
    """
    위험도 레벨 정보 반환
    
    Args:
        cdi: 혼잡도 지수
        
    Returns:
        dict: 위험도 정보
    """
    # CDI 값에 따라 레벨 결정
    # RISK_LEVELS는 threshold 순으로 정렬되어 있다고 가정하거나 순회하며 확인
    
    selected_level = "DANGER" # 기본값
    
    # 임계값 비교 (SAFE < CAUTION < WARNING < DANGER)
    if cdi < RISK_LEVELS["SAFE"]["threshold"]:
        selected_level = "SAFE"
    elif cdi < RISK_LEVELS["CAUTION"]["threshold"]:
        selected_level = "CAUTION"
    elif cdi < RISK_LEVELS["WARNING"]["threshold"]:
        selected_level = "WARNING"
    else:
        selected_level = "DANGER"
        
    info = RISK_LEVELS[selected_level].copy()
    info["level"] = selected_level
    info["cdi"] = cdi
    info["cdi_percent"] = cdi * 100
    
    return info
