"""
간단한 테스트 스크립트 - 모듈 import 확인
"""
import sys
import os

print("현재 작업 디렉토리:", os.getcwd())
print("\n파일 존재 확인:")
files = ['app.py', 'crowd_detect.py', 'density.py', 'direction.py', 'utils.py']
for f in files:
    exists = os.path.exists(f)
    print(f"  {f}: {'✓' if exists else '✗'}")

print("\n모듈 import 테스트:")
try:
    from crowd_detect import CrowdDetector
    print("  ✓ crowd_detect")
except Exception as e:
    print(f"  ✗ crowd_detect: {e}")

try:
    from density import calculate_cdi, get_risk_level_info
    print("  ✓ density")
except Exception as e:
    print(f"  ✗ density: {e}")

try:
    from direction import get_direction_info
    print("  ✓ direction")
except Exception as e:
    print(f"  ✗ direction: {e}")

try:
    from utils import create_grid, count_people_in_grid
    print("  ✓ utils")
except Exception as e:
    print(f"  ✗ utils: {e}")

try:
    import streamlit
    print(f"  ✓ streamlit (버전: {streamlit.__version__})")
except Exception as e:
    print(f"  ✗ streamlit: {e}")

try:
    import cv2
    print(f"  ✓ opencv-python (버전: {cv2.__version__})")
except Exception as e:
    print(f"  ✗ opencv-python: {e}")

try:
    from ultralytics import YOLO
    print("  ✓ ultralytics")
except Exception as e:
    print(f"  ✗ ultralytics: {e}")

print("\n" + "="*50)
print("테스트 완료!")

