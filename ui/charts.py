"""
차트 및 그래프 컴포넌트
"""
import altair as alt
import pandas as pd
import streamlit as st

def render_person_count_chart(data_history):
    """
    시간별 인원수 추이 차트 (Line Chart)
    
    Args:
        data_history: [{'time': 'HH:MM:SS', 'count': 10, 'cdi': 0.5}, ...]
    """
    if not data_history:
        st.info("데이터 수집 중...")
        return

    df = pd.DataFrame(data_history)
    
    # 최근 30개 데이터만 표시
    if len(df) > 30:
        df = df.tail(30)
        
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('time', title='시간', axis=alt.Axis(labels=False)), # 라벨 너무 많으면 지저분하므로 숨김
        y=alt.Y('count', title='인원 수'),
        tooltip=['time', 'count', 'cdi']
    ).properties(
        height=200,
        title="실시간 인원 추이"
    ).configure_axis(
        grid=True,
        gridColor='#333'
    ).configure_view(
        strokeWidth=0
    )
    
    st.altair_chart(chart, use_container_width=True)

def render_risk_gauge(cdi):
    """
    위험도 게이지 차트 (Altair로 도넛 차트 흉내)
    """
    # 게이지 차트는 Altair로 구현하기 복잡하므로, 
    # Streamlit의 progress bar나 metric으로 대체하고 CSS로 꾸미는 것이 더 깔끔함.
    # 여기서는 CDI 값을 시각적으로 보여주는 바 차트로 구현
    
    df = pd.DataFrame({'label': ['CDI'], 'value': [cdi]})
    
    # 색상 결정
    color = "#4CAF50"
    if cdi >= 0.8: color = "#F44336"
    elif cdi >= 0.6: color = "#FF9800"
    elif cdi >= 0.3: color = "#FFC107"
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('value', scale=alt.Scale(domain=[0, 1]), title='혼잡도 지수 (0~1)'),
        y=alt.Y('label', title=None, axis=None),
        color=alt.value(color),
        tooltip=['value']
    ).properties(
        height=50
    )
    
    st.altair_chart(chart, use_container_width=True)

def render_grid_stats(grid_counts, grid_size=(3, 3)):
    """
    그리드별 인원 통계 바 차트
    """
    if not grid_counts:
        return
        
    # 데이터 변환
    data = []
    rows, cols = grid_size
    for idx, count in enumerate(grid_counts):
        # 위치 이름 생성
        row = idx // cols
        col = idx % cols
        name = f"구역 {idx+1}"
        data.append({'zone': name, 'count': count})
        
    df = pd.DataFrame(data)
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('zone', title='구역', sort=None),
        y=alt.Y('count', title='인원 수'),
        color=alt.Color('count', scale=alt.Scale(scheme='yelloworangered'), legend=None),
        tooltip=['zone', 'count']
    ).properties(
        height=200,
        title="구역별 인원 분포"
    )
    
    st.altair_chart(chart, use_container_width=True)
