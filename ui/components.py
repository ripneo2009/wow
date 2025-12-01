"""
UI 컴포넌트 모듈
- 사이드바, 알림, 레이아웃 등
"""
import streamlit as st
from config import DEFAULT_GRID_SIZE, DEFAULT_CONF_THRESHOLD

def render_sidebar():
    """
    사이드바 렌더링 및 설정값 반환
    
    Returns:
        settings: 설정값 딕셔너리
    """
    with st.sidebar:
        st.header("⚙️ 시스템 설정")
        
        st.subheader("검출 설정")
        conf_threshold = st.slider(
            "검출 신뢰도 (Confidence)",
            min_value=0.1,
            max_value=0.9,
            value=DEFAULT_CONF_THRESHOLD,
            step=0.05,
            help="값이 높을수록 확실한 사람만 검출합니다."
        )
        
        st.subheader("분석 설정")
        grid_option = st.selectbox(
            "그리드 크기",
            options=["2x2", "3x3", "4x4"],
            index=1
        )
        
        # 그리드 크기 파싱
        grid_map = {"2x2": (2, 2), "3x3": (3, 3), "4x4": (4, 4)}
        grid_size = grid_map[grid_option]
        
        st.subheader("알림 설정")
        enable_alert = st.toggle("위험 알림 켜기", value=True)
        alert_sound = st.toggle("경고음 재생", value=False)
        
        st.markdown("---")
        st.markdown("### ℹ️ 정보")
        st.info(
            """
            **AI 군중 위험도 감지 시스템**
            
            CCTV 영상을 분석하여 실시간으로
            군중 밀집도와 위험도를 감지합니다.
            """
        )
        
        return {
            "conf_threshold": conf_threshold,
            "grid_size": grid_size,
            "enable_alert": enable_alert,
            "alert_sound": alert_sound
        }

def render_alert(risk_level, message, enable_sound=False):
    """
    위험 알림 렌더링
    """
    if risk_level in ["WARNING", "DANGER"]:
        type_map = {"WARNING": "warning", "DANGER": "error"}
        func = getattr(st, type_map[risk_level])
        func(f"🚨 {message}")
        
        if enable_sound and risk_level == "DANGER":
            # HTML5 Audio로 경고음 재생 (비프음 예시)
            # 실제 파일이 없으므로 base64나 온라인 URL 사용 가능하지만, 
            # 여기서는 간단히 텍스트로만 처리하거나 비프음 스크립트 삽입
            st.markdown("""
                <audio autoplay>
                    <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
                </audio>
            """, unsafe_allow_html=True)

def render_dashboard_metrics(person_count, cdi, risk_info):
    """
    대시보드 상단 메트릭 렌더링
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<p class="metric-label">현재 인원</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-value">{person_count}명</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<p class="metric-label">혼잡도 지수 (CDI)</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-value">{cdi:.2f}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        risk_color = risk_info["hex"]
        st.markdown(f'<div class="dashboard-card" style="border-bottom: 4px solid {risk_color};">', unsafe_allow_html=True)
        st.markdown('<p class="metric-label">위험도 레벨</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-value" style="color: {risk_color};">{risk_info["label"]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
