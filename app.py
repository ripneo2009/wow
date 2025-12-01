"""
CCTV 군중 위험도 감지 시스템 메인 애플리케이션
"""
import os
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"
import streamlit as st
import cv2
import time
import os
import pandas as pd
from datetime import datetime
import torch
torch.serialization.add_safe_globals([__import__("ultralytics").nn.tasks.DetectionModel])

# 모듈 임포트
from config import PROJECT_TITLE, PROJECT_ICON, LAYOUT, SAMPLE_VIDEO_PATH
from modules.detector import CrowdDetector
from modules.density import calculate_cdi, get_risk_level_info
from modules.direction import get_direction_info
from utils.grid import create_grid, count_people_in_grid
from utils.heatmap import create_heatmap
from utils.logger import setup_logger
from ui.styles import apply_custom_styles, get_risk_badge_html
from ui.components import render_sidebar, render_alert, render_dashboard_metrics
from ui.charts import render_person_count_chart, render_grid_stats

# 로거 설정
logger = setup_logger()

# 페이지 설정
st.set_page_config(
    page_title=PROJECT_TITLE,
    page_icon=PROJECT_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# 스타일 적용
apply_custom_styles()

def init_session_state():
    """세션 상태 초기화"""
    if 'detector' not in st.session_state:
        st.session_state.detector = None
    if 'video_path' not in st.session_state:
        st.session_state.video_path = None
    if 'is_playing' not in st.session_state:
        st.session_state.is_playing = False
    if 'current_frame' not in st.session_state:
        st.session_state.current_frame = 0
    if 'data_history' not in st.session_state:
        st.session_state.data_history = []
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None

def load_model():
    """모델 로드 (캐싱)"""
    if st.session_state.detector is None:
        try:
            with st.spinner("AI 모델 로딩 중..."):
                st.session_state.detector = CrowdDetector()
            logger.info("모델 로드 성공")
        except Exception as e:
            st.error(f"모델 로드 실패: {e}")
            logger.error(f"모델 로드 실패: {e}")
            st.stop()

def save_log(data_history):
    """분석 로그 저장"""
    if not data_history:
        return
        
    df = pd.DataFrame(data_history)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/analysis_{timestamp}.csv"
    
    try:
        os.makedirs("logs", exist_ok=True)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        logger.info(f"로그 저장 완료: {filename}")
        return filename
    except Exception as e:
        logger.error(f"로그 저장 실패: {e}")
        return None

def main():
    init_session_state()
    load_model()
    
    # 사이드바 렌더링
    settings = render_sidebar()
    
    # 메인 헤더
    st.title(f"{PROJECT_ICON} {PROJECT_TITLE}")
    st.markdown("---")
    
    # 영상 업로드 섹션
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader("CCTV 영상 업로드", type=['mp4', 'avi', 'mov'])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("▶️ 데모 영상 실행", type="secondary", use_container_width=True):
            if os.path.exists(SAMPLE_VIDEO_PATH):
                st.session_state.video_path = SAMPLE_VIDEO_PATH
                st.session_state.current_frame = 0
                st.session_state.data_history = []
                st.rerun()
            else:
                st.error("데모 영상을 찾을 수 없습니다.")
    
    # 영상 경로 설정
    if uploaded_file:
        # 임시 파일 저장
        os.makedirs("temp", exist_ok=True)
        temp_path = os.path.join("temp", uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.video_path = temp_path
    
    # 분석 화면
    if st.session_state.video_path:
        cap = cv2.VideoCapture(st.session_state.video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # 레이아웃 분할 (좌: 영상, 우: 대시보드)
        dash_col1, dash_col2 = st.columns([1.5, 1])
        
        # ---------------------------------------------------------
        # 분석 로직
        # ---------------------------------------------------------
        # 현재 프레임 읽기
        cap.set(cv2.CAP_PROP_POS_FRAMES, st.session_state.current_frame)
        ret, frame = cap.read()
        
        if ret:
            # 1. 사람 검출
            boxes, frame_with_boxes, person_count = st.session_state.detector.detect_people(
                frame, conf_threshold=settings['conf_threshold']
            )
            
            # 2. 그리드 분석
            grid_regions, frame_with_grid = create_grid(frame_with_boxes, settings['grid_size'])
            grid_counts = count_people_in_grid(boxes, grid_regions)
            
            # 3. 위험도 계산
            frame_area = width * height
            cdi = calculate_cdi(person_count, frame_area, grid_counts)
            risk_info = get_risk_level_info(cdi)
            
            # 4. 방향 추천
            direction_info = get_direction_info(grid_counts, settings['grid_size'])
            
            # 5. 히트맵 생성
            frame_final = create_heatmap(frame_with_grid, grid_counts, grid_regions, settings['grid_size'])
            
            # 데이터 기록
            current_time = datetime.now().strftime("%H:%M:%S")
            st.session_state.data_history.append({
                "time": current_time,
                "count": person_count,
                "cdi": cdi,
                "risk": risk_info["level"]
            })
            
            # ---------------------------------------------------------
            # UI 렌더링
            # ---------------------------------------------------------
            
            # [좌측] 영상 및 컨트롤
            with dash_col1:
                st.markdown('<div class="section-header">실시간 모니터링</div>', unsafe_allow_html=True)
                
                # 위험도에 따른 테두리 효과
                border_class = ""
                if settings['enable_alert'] and risk_info['level'] == 'DANGER':
                    border_class = "risk-alert-red"
                
                # 영상 표시
                frame_rgb = cv2.cvtColor(frame_final, cv2.COLOR_BGR2RGB)
                st.markdown(f'<div class="{border_class}">', unsafe_allow_html=True)
                st.image(frame_rgb, use_container_width=True, channels="RGB")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 컨트롤 패널
                c1, c2, c3 = st.columns([1, 2, 1])
                with c1:
                    if st.button("⏮️ 5초 전", use_container_width=True):
                        st.session_state.current_frame = max(0, st.session_state.current_frame - int(fps*5))
                        st.rerun()
                with c2:
                    play_label = "⏸️ 일시정지" if st.session_state.is_playing else "▶️ 재생 / 분석"
                    if st.button(play_label, type="primary", use_container_width=True):
                        st.session_state.is_playing = not st.session_state.is_playing
                        st.rerun()
                with c3:
                    if st.button("⏭️ 5초 후", use_container_width=True):
                        st.session_state.current_frame = min(total_frames-1, st.session_state.current_frame + int(fps*5))
                        st.rerun()
                        
                # 진행바
                st.progress(st.session_state.current_frame / total_frames)
                st.caption(f"Frame: {st.session_state.current_frame} / {total_frames}")

            # [우측] 대시보드
            with dash_col2:
                st.markdown('<div class="section-header">분석 대시보드</div>', unsafe_allow_html=True)
                
                # 상단 메트릭
                render_dashboard_metrics(person_count, cdi, risk_info)
                
                # 알림 표시
                if settings['enable_alert']:
                    render_alert(risk_info['level'], 
                               f"위험 감지! 현재 인원 {person_count}명 (CDI: {cdi:.2f})", 
                               settings['alert_sound'])
                
                # 차트 영역
                st.markdown("### 📈 실시간 추이")
                render_person_count_chart(st.session_state.data_history)
                
                st.markdown("### 🗺️ 구역별 분포")
                render_grid_stats(grid_counts, settings['grid_size'])
                
                # 안전 방향 안내
                st.markdown("### 🧭 추천 이동 방향")
                st.info(f"**{direction_info['direction_arrow']} {direction_info['direction_text']}** 으로 이동하세요.")
                
                # 로그 저장 버튼
                if st.button("💾 분석 결과 저장 (CSV)", use_container_width=True):
                    filename = save_log(st.session_state.data_history)
                    if filename:
                        st.success(f"저장 완료: {filename}")
                    else:
                        st.warning("저장할 데이터가 없습니다.")

        cap.release()
        
        # 자동 재생 로직
        if st.session_state.is_playing and st.session_state.current_frame < total_frames - 1:
            st.session_state.current_frame += 1 # 프레임 스킵 없이 1씩 증가 (속도 조절 필요 시 변경)
            time.sleep(0.01) # 너무 빠르면 UI 갱신이 못따라감
            st.rerun()
            
    else:
        # 초기 화면 (영상이 없을 때)
        st.info("좌측 상단의 'Browse files'를 눌러 영상을 업로드하거나, '데모 영상 실행' 버튼을 누르세요.")
        
        # 사용 가이드
        st.markdown("""
        ### 📖 사용 가이드
        1. **영상 업로드**: 분석할 CCTV 영상을 업로드합니다.
        2. **설정 조절**: 사이드바에서 감도, 그리드 크기 등을 조절합니다.
        3. **분석 시작**: 재생 버튼을 눌러 실시간 분석을 시작합니다.
        4. **결과 확인**: 대시보드에서 위험도와 통계를 확인합니다.
        """)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error("애플리케이션 실행 중 오류가 발생했습니다.")
        st.error(f"Error: {str(e)}")
        logger.error(f"App Crash: {str(e)}")
