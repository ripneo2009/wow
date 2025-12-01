@echo off
chcp 65001 >nul
title AI 군중 위험도 감지 시스템
color 0A

echo.
echo ============================================================
echo    AI 군중 위험도 감지 시스템 (Upgrade Ver.)
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/3] 필수 패키지 확인 중...
pip install -r requirements.txt
if errorlevel 1 (
    echo [오류] 패키지 설치 실패!
    pause
    exit /b 1
)
echo.

echo [2/3] 실행 준비 완료
echo.

echo [3/3] 애플리케이션 시작...
echo.
echo 브라우저가 자동으로 열립니다.
echo 실행 주소: http://localhost:8501
echo.
echo 종료하려면 Ctrl+C를 누르세요.
echo ============================================================
echo.

streamlit run app.py
pause
