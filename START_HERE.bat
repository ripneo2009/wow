@echo off
chcp 65001 >nul
title CCTV 군중 위험도 감지 시스템
color 0A

echo.
echo ============================================================
echo    CCTV 영상 기반 AI 군중 위험도 감지 시스템
echo ============================================================
echo.

REM 현재 스크립트가 있는 디렉토리로 이동
cd /d "%~dp0"

echo [1/3] 현재 위치 확인...
echo 디렉토리: %CD%
echo.

echo [2/3] 필수 파일 확인...
if not exist "app.py" (
    echo [오류] app.py 파일을 찾을 수 없습니다!
    echo 현재 위치: %CD%
    pause
    exit /b 1
)
echo [확인] app.py 파일 발견
echo.

echo [3/3] Streamlit 애플리케이션 시작...
echo.
echo ============================================================
echo 브라우저가 자동으로 열립니다.
echo URL: http://localhost:8501
echo.
echo 중지하려면 이 창에서 Ctrl+C를 누르세요.
echo ============================================================
echo.

REM Streamlit 실행
streamlit run app.py

if errorlevel 1 (
    echo.
    echo ============================================================
    echo [오류] 실행 중 문제가 발생했습니다!
    echo.
    echo 가능한 원인:
    echo 1. Streamlit이 설치되지 않았습니다
    echo    해결: pip install streamlit
    echo.
    echo 2. 필요한 패키지가 설치되지 않았습니다
    echo    해결: pip install -r requirements.txt
    echo.
    echo 3. 포트 8501이 이미 사용 중입니다
    echo    해결: 다른 터미널에서 실행 중인 streamlit을 종료하세요
    echo ============================================================
    echo.
    pause
)

