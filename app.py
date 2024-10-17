import ntplib
from datetime import datetime

from fastapi import FastAPI
from homework import homework
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
time_difference = 0

NTP_SERVER = 'pool.ntp.org'


def sync_time_with_ntp_server():

    global time_difference
    global NTP_SERVER

    try:
        # 使用 ntplib 來創建 NTP 客戶端
        ntp_client = ntplib.NTPClient()

        # 向 pool.ntp.org 發送請求，獲取 NTP 響應數據
        response = ntp_client.request(NTP_SERVER)

        # 獲取 NTP 伺服器的時間戳（秒數）
        ntp_time = response.tx_time

        # 獲取本地時間的時間戳（秒數）
        local_time = datetime.now().timestamp()

        # 計算本地時間與 NTP 伺服器時間之間的差異（秒數）
        time_difference = local_time - ntp_time

        print(f"NTP time: {ntp_time} seconds.")
        print(f"local time: {local_time} seconds.")
        print(f"Time difference: {time_difference} seconds.")

    except Exception as e:
        return {"error": str(e)}

def get_time_from_ntp_server():

    global time_difference
    global NTP_SERVER

    try:
        # 使用 ntplib 來創建 NTP 客戶端
        ntp_client = ntplib.NTPClient()

        # 向 pool.ntp.org 發送請求，獲取 NTP 響應數據
        response = ntp_client.request(NTP_SERVER)

        # 獲取 NTP 伺服器的時間戳（秒數）
        ntp_time = response.tx_time

        # 獲取本地時間的時間戳（秒數）
        local_time = datetime.now().timestamp() - time_difference

        print(f"NTP time: {ntp_time} seconds.")
        print(f"local time: {local_time} seconds.")
        print(f"Time difference: {time_difference} seconds.")

    except Exception as e:
        print(f"An error occurred: {e}")


@app.on_event("startup")
async def startup_event():
    # 啟動時與 NTP 伺服器同步時間
    sync_time_with_ntp_server()



@app.get("/get_time")
def get_time():
    global time_difference
    timestamp = datetime.now().timestamp() - time_difference
    return {"timeStamp": datetime.now().timestamp() - time_difference,
            "formatted_time": datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')}

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