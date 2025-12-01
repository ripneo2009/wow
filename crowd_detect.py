"""
YOLO 기반 사람 검출 모듈
- ultralytics YOLOv8n 모델 사용
- 사람 클래스(ID: 0)만 검출
"""

from ultralytics import YOLO
import cv2
import numpy as np


class CrowdDetector:
    """YOLO를 사용한 군중 검출 클래스"""
    
    def __init__(self, model_path='yolov8n.pt'):
        """
        초기화
        
        Args:
            model_path: YOLO 모델 경로 (기본값: 'yolov8n.pt')
        """
        self.model = YOLO(model_path)
        self.person_class_id = 0  # COCO 데이터셋에서 사람 클래스 ID는 0
    
    def detect_people(self, frame, conf_threshold=0.25):
        """
        프레임에서 사람을 검출
        
        Args:
            frame: 입력 프레임 (numpy array, BGR 형식)
            conf_threshold: 신뢰도 임계값 (기본값: 0.25)
        
        Returns:
            boxes: 검출된 사람 박스 리스트 [(x1, y1, x2, y2), ...]
            frame_with_boxes: 박스가 그려진 프레임
            person_count: 검출된 사람 수
        """
        # YOLO 모델로 검출 수행
        results = self.model(frame, conf=conf_threshold, verbose=False)
        
        boxes = []
        frame_with_boxes = frame.copy()
        
        # 검출 결과에서 사람만 필터링
        for result in results:
            boxes_data = result.boxes
            
            for box in boxes_data:
                # 클래스 ID 확인 (0 = person)
                class_id = int(box.cls[0])
                
                if class_id == self.person_class_id:
                    # 박스 좌표 추출 (xyxy 형식)
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    
                    boxes.append((x1, y1, x2, y2))
                    
                    # 박스 그리기
                    cv2.rectangle(frame_with_boxes, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # 신뢰도 표시
                    conf = float(box.conf[0])
                    label = f"Person {conf:.2f}"
                    cv2.putText(frame_with_boxes, label, (x1, y1 - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        person_count = len(boxes)
        
        return boxes, frame_with_boxes, person_count
    
    def process_video_frame(self, video_path, frame_number):
        """
        비디오에서 특정 프레임을 읽어서 처리
        
        Args:
            video_path: 비디오 파일 경로
            frame_number: 프레임 번호
        
        Returns:
            frame: 프레임 이미지 (없으면 None)
        """
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            return frame
        return None

