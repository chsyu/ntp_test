import requests
from datetime import datetime

from fastapi import FastAPI
from homework import homework
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
time_difference = 0

def sync_time_with_ntp_server(ntp_server_url="http://host.docker.internal:4000/get_time"):

    global time_difference

    try:
        # 向 NTP-like 伺服器發送請求，獲取伺服器時間
        response = requests.get(ntp_server_url)
        if response.status_code == 200:
            ntp_data = response.json()
            server_time = ntp_data['timestamp']
            print(f"Received server time: {server_time}")
            # 取得當前本地時間戳
            local_time = datetime.now().timestamp()
            print(f"Received local time: {local_time}")
            # 計算並儲存伺服器和本地的時間差異
            time_difference = server_time - local_time
            print(f"Time difference: {time_difference} seconds")

        else:
            print(f"Failed to get time from NTP server: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_time_from_ntp_server(ntp_server_url="http://host.docker.internal:4000/get_time"):

    global time_difference

    try:
        # 向 NTP-like 伺服器發送請求，獲取伺服器時間
        response = requests.get(ntp_server_url)
        if response.status_code == 200:
            ntp_data = response.json()
            server_time = ntp_data['timestamp']
            print(f"Received server time: {server_time}")
            print(f"Time difference: {time_difference} seconds")
            local_time = datetime.now().timestamp() + time_difference
            print(f"Received local time: {local_time}")
            print(f"Time error: {server_time-local_time} seconds")
        else:
            print(f"Failed to get time from NTP server: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


@app.on_event("startup")
async def startup_event():
    # 啟動時與 NTP 伺服器同步時間
    sync_time_with_ntp_server()


@app.get("/check_time")
def check_time():
    get_time_from_ntp_server()
    return {"message": "Time checked successfully!"}


@app.get("/sync_time")
def sync_time():
    sync_time_with_ntp_server()
    return {"message": "Time synchronized successfully!"}

@app.get("/homework")
def root():
    return homework


origins = [
    'http://localhost:5173',
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)