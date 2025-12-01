@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Streamlit 실행 중...
streamlit run app.py
pause

