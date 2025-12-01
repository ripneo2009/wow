"""
유틸리티 함수 모듈
- 그리드 생성 및 관리
- 히트맵 생성
- 공용 함수들
"""

import cv2
import numpy as np


def create_grid(frame, grid_size=(3, 3)):
    """
    프레임을 그리드로 나누고 각 구역의 좌표를 반환
    
    Args:
        frame: 입력 프레임 (numpy array)
        grid_size: 그리드 크기 (rows, cols) 기본값 (3, 3)
    
    Returns:
        grid_regions: 각 그리드 구역의 좌표 리스트 [(x1, y1, x2, y2), ...]
        frame_with_grid: 그리드가 그려진 프레임
    """
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


def create_heatmap(frame, grid_counts, grid_regions, grid_size=(3, 3)):
    """
    그리드별 사람 수를 기반으로 히트맵 생성
    
    Args:
        frame: 원본 프레임
        grid_counts: 각 그리드 구역의 사람 수 리스트
        grid_regions: 그리드 구역 좌표 리스트
        grid_size: 그리드 크기
    
    Returns:
        heatmap: 히트맵 이미지
    """
    h, w = frame.shape[:2]
    heatmap = np.zeros((h, w), dtype=np.float32)
    
    rows, cols = grid_size
    
    # 각 그리드 구역에 사람 수에 비례한 값 할당
    max_count = max(grid_counts) if grid_counts else 1
    
    for idx, (gx1, gy1, gx2, gy2) in enumerate(grid_regions):
        count = grid_counts[idx]
        intensity = count / max_count if max_count > 0 else 0
        
        # 해당 구역에 강도 값 할당
        heatmap[gy1:gy2, gx1:gx2] = intensity
    
    # 0-255 범위로 정규화
    heatmap = (heatmap * 255).astype(np.uint8)
    
    # 컬러맵 적용 (JET 컬러맵 사용)
    heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    # 원본 프레임과 블렌딩
    blended = cv2.addWeighted(frame, 0.6, heatmap_colored, 0.4, 0)
    
    return blended


def get_grid_position_name(idx, grid_size=(3, 3)):
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
    
    if row < len(row_names) and col < len(col_names):
        if row == 1 and col == 1:  # 정중앙
            return "중앙"
        elif row == 1:  # 중앙 행
            return f"{col_names[col]}"
        elif col == 1:  # 중앙 열
            return f"{row_names[row]}"
        else:
            return f"{row_names[row]}-{col_names[col]}"
    
    return f"구역{idx}"

