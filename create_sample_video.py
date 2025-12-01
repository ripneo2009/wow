"""
테스트용 샘플 비디오 생성 스크립트
사람이 있는 것처럼 보이는 간단한 테스트 영상을 생성합니다.
"""

import cv2
import numpy as np
import os

def create_sample_video(output_path="assets/sample_video.mp4", duration_seconds=10, fps=30):
    """
    테스트용 샘플 비디오 생성
    
    Args:
        output_path: 출력 비디오 경로
        duration_seconds: 영상 길이 (초)
        fps: 프레임 레이트
    """
    # assets 디렉토리 생성
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 비디오 작성자 초기화
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    total_frames = duration_seconds * fps
    
    print(f"샘플 비디오 생성 중... ({duration_seconds}초, {fps} FPS)")
    
    for i in range(total_frames):
        # 배경 생성 (회색 톤)
        frame = np.random.randint(50, 100, (height, width, 3), dtype=np.uint8)
        
        # 시간에 따라 움직이는 도형들 (사람처럼 보이도록)
        # 프레임 번호에 따라 위치 변경
        t = i / fps
        
        # 여러 개의 "사람" 도형 추가
        num_people = 3 + int(np.sin(t) * 2)  # 1~5명 사이에서 변동
        
        for j in range(num_people):
            # 각 사람의 위치 계산 (움직임 시뮬레이션)
            x = int((width // 4) + (width // 2) * (j / num_people) + 50 * np.sin(t + j))
            y = int((height // 4) + (height // 2) * (j / num_people) + 30 * np.cos(t + j))
            
            # 사람 모양의 직사각형 (몸통)
            cv2.rectangle(frame, 
                         (x - 20, y - 40), 
                         (x + 20, y + 40), 
                         (100 + j * 30, 100 + j * 30, 100 + j * 30), 
                         -1)
            
            # 머리 (원)
            cv2.circle(frame, (x, y - 50), 15, (120 + j * 20, 120 + j * 20, 120 + j * 20), -1)
        
        # 그리드 선 표시 (3×3)
        for k in range(1, 3):
            cv2.line(frame, (0, height * k // 3), (width, height * k // 3), (200, 200, 200), 1)
            cv2.line(frame, (width * k // 3, 0), (width * k // 3, height), (200, 200, 200), 1)
        
        out.write(frame)
        
        if (i + 1) % 30 == 0:
            print(f"진행률: {(i + 1) / total_frames * 100:.1f}%")
    
    out.release()
    print(f"✅ 샘플 비디오 생성 완료: {output_path}")
    print(f"   - 길이: {duration_seconds}초")
    print(f"   - 해상도: {width}x{height}")
    print(f"   - FPS: {fps}")

if __name__ == "__main__":
    create_sample_video()

