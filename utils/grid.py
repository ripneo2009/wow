"""
그리드 유틸리티 모듈
- 프레임 그리드 분할 및 관리
"""
import cv2
import numpy as np
from config import DEFAULT_GRID_SIZE

def create_grid(frame, grid_size=DEFAULT_GRID_SIZE):
    """
    프레임을 그리드로 나누고 각 구역의 좌표를 반환
    
    Args:
        frame: 입력 프레임 (numpy array)
        grid_size: 그리드 크기 (rows, cols)
    
    Returns:
        grid_regions: 각 그리드 구역의 좌표 리스트 [(x1, y1, x2, y2), ...]
        frame_with_grid: 그리드가 그려진 프레임
    """
    if frame is None:
        return [], None
        
    h, w = frame.shape[:2]
    rows, cols = grid_size
    
    grid_regions = []
    frame_with_grid = frame.copy()
    
    # 그리드 선 그리기
    for i in range(1, rows):
        y = int(h * i / rows)
        cv2.line(frame_with_grid, (0, y), (w, y), (255, 255, 255), 2)
    
    for j in range(1, cols):
        x = int(w * j / cols)
        cv2.line(frame_with_grid, (x, 0), (x, h), (255, 255, 255), 2)
    
    # 각 그리드 구역의 좌표 계산
    cell_h = h / rows
    cell_w = w / cols
    
    for i in range(rows):
        for j in range(cols):
            x1 = int(j * cell_w)
            y1 = int(i * cell_h)
            x2 = int((j + 1) * cell_w)
            y2 = int((i + 1) * cell_h)
            grid_regions.append((x1, y1, x2, y2))
    
    return grid_regions, frame_with_grid

def get_grid_position_name(idx, grid_size=DEFAULT_GRID_SIZE):
    """
    그리드 인덱스를 위치 이름으로 변환
    
    Args:
        idx: 그리드 인덱스 (0부터 시작)
        grid_size: 그리드 크기
    
    Returns:
        position_name: 위치 이름 (예: "상단-좌측", "중앙-우측")
    """
    rows, cols = grid_size
    row = idx // cols
    col = idx % cols
    
    row_names = ["상단", "중앙", "하단"]
    col_names = ["좌측", "중앙", "우측"]
    
    # 3x3 그리드에 최적화된 이름 반환
    if rows == 3 and cols == 3:
        if row == 1 and col == 1:  # 정중앙
            return "중앙"
        elif row == 1:  # 중앙 행
            return f"{col_names[col]}"
        elif col == 1:  # 중앙 열
            return f"{row_names[row]}"
        else:
            return f"{row_names[row]}-{col_names[col]}"
    
    # 일반적인 경우
    return f"구역 {idx+1} ({row+1}행 {col+1}열)"


def count_people_in_grid(boxes, grid_regions):
    """
    각 그리드 구역에 있는 사람 수를 계산
    
    Args:
        boxes: YOLO 검출 박스 리스트 [(x1, y1, x2, y2), ...]
        grid_regions: 그리드 구역 좌표 리스트
    
    Returns:
        grid_counts: 각 그리드 구역의 사람 수 리스트
    """
    grid_counts = [0] * len(grid_regions)
    
    for box in boxes:
        # 박스 중심점 계산
        box_x1, box_y1, box_x2, box_y2 = box
        center_x = (box_x1 + box_x2) / 2
        center_y = (box_y1 + box_y2) / 2
        
        # 어느 그리드 구역에 속하는지 확인
        for idx, (gx1, gy1, gx2, gy2) in enumerate(grid_regions):
            if gx1 <= center_x < gx2 and gy1 <= center_y < gy2:
                grid_counts[idx] += 1
                break
    
    return grid_counts
