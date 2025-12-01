"""
히트맵 유틸리티 모듈
- 인원 분포 시각화
"""
import cv2
import numpy as np

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
    if frame is None or not grid_counts:
        return frame
        
    h, w = frame.shape[:2]
    heatmap = np.zeros((h, w), dtype=np.float32)
    
    # 각 그리드 구역에 사람 수에 비례한 값 할당
    max_count = max(grid_counts) if grid_counts else 1
    if max_count == 0:
        max_count = 1
    
    for idx, (gx1, gy1, gx2, gy2) in enumerate(grid_regions):
        if idx < len(grid_counts):
            count = grid_counts[idx]
            intensity = count / max_count
            
            # 해당 구역에 강도 값 할당
            heatmap[gy1:gy2, gx1:gx2] = intensity
    
    # 0-255 범위로 정규화
    heatmap = (heatmap * 255).astype(np.uint8)
    
    # 컬러맵 적용 (JET 컬러맵 사용)
    heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    # 원본 프레임과 블렌딩
    blended = cv2.addWeighted(frame, 0.6, heatmap_colored, 0.4, 0)
    
    return blended
