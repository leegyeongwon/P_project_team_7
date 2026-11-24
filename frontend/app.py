import os
import requests
import streamlit as st

# docker-compose.yml에 설정된 API_BASE_URL 사용 (기본값 설정)
BACKEND_API_BASE_URL = os.getenv("BACKEND_API_BASE_URL", "http://backend:8000")

st.title("FastAPI 연동 테스트")

# 테스트 신호를 보내는 버튼
if st.button("FastAPI에 신호 보내기"):
    try:
        # http://backend:8000/signal 로 GET 요청 전송
        response = requests.get(f"{BACKEND_API_BASE_URL}/check_signal", timeout=5)
        response.raise_for_status()

        data = response.json()

        # 응답 결과를 출력하는 창
        st.success(f"서버 응답: {data['message']}")

    except requests.exceptions.ConnectionError:
        st.error(
            "FastAPI 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요."
        )
    except Exception as e:
        st.error(f"오류 발생: {e}")