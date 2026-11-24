from fastapi import FastAPI

app = FastAPI()


@app.get("/check_signal")
def send_signal():
    # 이 부분에 DB 조회 로직을 추가
    return {"message": "수신 완료"}
