"""
안전 방향 추천 모듈
"""
import numpy as np

def find_safest_direction(grid_counts, grid_size=(3, 3)):
    """
    가장 안전한 방향(사람 수가 가장 적은 구역) 찾기
    
    Args:
        grid_counts: 각 그리드 구역의 사람 수 리스트
        grid_size: 그리드 크기 (rows, cols)
    
    Returns:
        safest_idx: 가장 안전한 구역 인덱스
        direction_text: 방향 텍스트
        direction_arrow: 방향 화살표
    """
    if not grid_counts or all(count == 0 for count in grid_counts):
        return None, "모든 구역이 안전합니다", "✓"
    
    rows, cols = grid_size
    
    # 사람 수가 가장 적은 구역 찾기
    min_count = min(grid_counts)
    safest_indices = [i for i, count in enumerate(grid_counts) if count == min_count]
    
    # 여러 구역이 같은 최소값을 가지면 첫 번째 것 선택 (추후 거리 기반 등으로 개선 가능)
    safest_idx = safest_indices[0]
    
    # 그리드 위치 계산
    row = safest_idx // cols
    col = safest_idx % cols
    
    # 방향 텍스트 생성
    direction_parts = []
    direction_arrow = ""
    
    # 행 방향 (상하)
    if row == 0:
        direction_parts.append("상단")
        direction_arrow = "↑"
    elif row == rows - 1:
        direction_parts.append("하단")
        direction_arrow = "↓"
    elif row < rows / 2:
        direction_parts.append("상단 쪽")
        direction_arrow = "↗"
    else:
        direction_parts.append("하단 쪽")
        direction_arrow = "↘"
    
    # 열 방향 (좌우)
    if col == 0:
        direction_parts.append("좌측")
        if not direction_arrow:
            direction_arrow = "←"
        else:
            direction_arrow = "↖" if row == 0 else "↙"
    elif col == cols - 1:
        direction_parts.append("우측")
        if not direction_arrow:
            direction_arrow = "→"
        else:
            direction_arrow = "↗" if row == 0 else "↘"
    elif col < cols / 2:
        direction_parts.append("좌측 쪽")
    else:
        direction_parts.append("우측 쪽")
    
    # 중앙인 경우
    if row == rows // 2 and col == cols // 2:
        direction_text = "중앙 지역"
        direction_arrow = "○"
    else:
        direction_text = f"{' '.join(direction_parts)}"
    
    return safest_idx, direction_text, direction_arrow

def get_direction_info(grid_counts, grid_size=(3, 3)):
    """
    안전 방향 정보 반환
    """
    safest_idx, direction_text, direction_arrow = find_safest_direction(grid_counts, grid_size)
    
    return {
        "safest_idx": safest_idx,
        "direction_text": direction_text,
        "direction_arrow": direction_arrow,
        "min_count": min(grid_counts) if grid_counts else 0
    }
