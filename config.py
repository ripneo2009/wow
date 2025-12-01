"""
프로젝트 설정 및 상수 정의
"""
import os

# ==========================================
# 기본 설정
# ==========================================
PROJECT_TITLE = "AI 군중 위험도 감지 시스템"
PROJECT_ICON = "🚨"
LAYOUT = "wide"

# ==========================================
# 경로 설정
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
MODEL_PATH = os.path.join(BASE_DIR, "yolov8n.pt")
SAMPLE_VIDEO_PATH = os.path.join(ASSETS_DIR, "sample_video.mp4")

# 디렉토리 생성
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# ==========================================
# 분석 설정
# ==========================================
# 그리드 설정
DEFAULT_GRID_SIZE = (3, 3)  # (rows, cols)

# 혼잡도 임계값 (CDI)
RISK_LEVELS = {
    "SAFE": {"threshold": 0.3, "color": (0, 255, 0), "label": "안전", "hex": "#4CAF50"},
    "CAUTION": {"threshold": 0.6, "color": (255, 255, 0), "label": "주의", "hex": "#FFC107"},
    "WARNING": {"threshold": 0.8, "color": (255, 165, 0), "label": "경고", "hex": "#FF9800"},
    "DANGER": {"threshold": 1.0, "color": (255, 0, 0), "label": "위험", "hex": "#F44336"}
}

# 검출 설정
DEFAULT_CONF_THRESHOLD = 0.25
DEFAULT_IOU_THRESHOLD = 0.45
PERSON_CLASS_ID = 0

# ==========================================
# UI 설정
# ==========================================
# 차트 색상
CHART_COLORS = ["#4CAF50", "#FFC107", "#FF9800", "#F44336"]
