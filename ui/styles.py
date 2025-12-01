"""
UI 스타일 및 CSS 정의
"""
import streamlit as st

def apply_custom_styles():
    """
    커스텀 CSS 적용
    """
    st.markdown("""
        <style>
        /* 전체 폰트 적용 (Pretendard, 없으면 sans-serif) */
        @import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css");
        
        html, body, [class*="css"] {
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', sans-serif;
        }
        
        /* 메인 컨테이너 패딩 조절 */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* 카드 스타일 (대시보드 패널) */
        .dashboard-card {
            background-color: #1E1E1E;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #333;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        /* 섹션 타이틀 */
        .section-header {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 15px;
            color: #E0E0E0;
            border-left: 4px solid #4CAF50;
            padding-left: 10px;
        }
        
        /* 위험도 알림 애니메이션 (RED) */
        @keyframes blink-red {
            0% { border-color: #F44336; box-shadow: 0 0 10px #F44336; }
            50% { border-color: transparent; box-shadow: none; }
            100% { border-color: #F44336; box-shadow: 0 0 10px #F44336; }
        }
        
        .risk-alert-red {
            border: 3px solid #F44336;
            animation: blink-red 1s infinite;
        }
        
        /* 위험도 배지 */
        .risk-badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: bold;
            color: white;
            text-align: center;
        }
        
        /* 메트릭 값 강조 */
        .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
            color: white;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #AAAAAA;
        }
        
        /* 버튼 스타일 오버라이드 */
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
        }
        
        /* 데이터프레임 스타일 */
        [data-testid="stDataFrame"] {
            background-color: #1E1E1E;
        }
        </style>
    """, unsafe_allow_html=True)

def get_risk_badge_html(level, label, color_hex):
    """
    위험도 배지 HTML 반환
    """
    return f"""
    <div style="background-color: {color_hex}; padding: 10px 20px; border-radius: 8px; text-align: center; color: white; font-weight: bold;">
        <span style="font-size: 1.5rem;">{label} ({level})</span>
    </div>
    """
