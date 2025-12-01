"""
YOLO 기반 객체 검출 모듈
- 사람 검출, 트래킹, 스무딩
"""
from ultralytics import YOLO
import cv2
import numpy as np
from collections import deque
from config import MODEL_PATH, PERSON_CLASS_ID, DEFAULT_CONF_THRESHOLD

class CrowdDetector:
    """YOLO를 사용한 군중 검출 클래스"""
    
    def __init__(self, model_path=MODEL_PATH):
        """
        초기화
        """
        try:
            self.model = YOLO(model_path)
        except Exception as e:
            print(f"모델 로드 실패: {e}")
            raise e
            
        self.person_class_id = PERSON_CLASS_ID
        
        # 박스 스무딩을 위한 히스토리 (ID별 최근 박스 좌표)
        # {track_id: deque([(x1, y1, x2, y2), ...], maxlen=5)}
        self.track_history = {}
        self.smoothing_window = 5
    
    def detect_people(self, frame, conf_threshold=DEFAULT_CONF_THRESHOLD, use_tracking=True):
        """
        프레임에서 사람을 검출
        
        Args:
            frame: 입력 프레임
            conf_threshold: 신뢰도 임계값
            use_tracking: 객체 트래킹 사용 여부 (ID 부여)
            
        Returns:
            boxes: 검출된 박스 리스트
            frame_with_boxes: 박스가 그려진 프레임
            person_count: 사람 수
        """
        if frame is None:
            return [], None, 0
            
        # YOLO 추론
        if use_tracking:
            # persist=True로 트래킹 유지
            results = self.model.track(frame, persist=True, conf=conf_threshold, verbose=False, classes=[self.person_class_id])
        else:
            results = self.model(frame, conf=conf_threshold, verbose=False, classes=[self.person_class_id])
        
        boxes = []
        frame_with_boxes = frame.copy()
        
        for result in results:
            boxes_data = result.boxes
            
            for box in boxes_data:
                # 좌표 추출
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                
                # 트래킹 ID (있으면)
                track_id = int(box.id[0]) if box.id is not None else None
                
                # 스무딩 적용 (트래킹 ID가 있을 때만)
                if track_id is not None:
                    if track_id not in self.track_history:
                        self.track_history[track_id] = deque(maxlen=self.smoothing_window)
                    
                    self.track_history[track_id].append((x1, y1, x2, y2))
                    
                    # 평균 좌표 계산
                    avg_box = np.mean(self.track_history[track_id], axis=0).astype(int)
                    x1, y1, x2, y2 = avg_box
                
                boxes.append((x1, y1, x2, y2))
                
                # 시각화
                color = (0, 255, 0) # Green
                cv2.rectangle(frame_with_boxes, (x1, y1), (x2, y2), color, 2)
                
                # 라벨 표시
                conf = float(box.conf[0])
                label = f"Person"
                if track_id is not None:
                    label += f" ID:{track_id}"
                
                cv2.putText(frame_with_boxes, label, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return boxes, frame_with_boxes, len(boxes)
