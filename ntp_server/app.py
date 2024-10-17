from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class TimeResponse(BaseModel):
    timestamp: float  # 返回 UNIX 時間戳記
    iso_format: str   # 返回 ISO 格式的時間

@app.get("/get_time", response_model=TimeResponse)
async def get_time():
    # 取得當前伺服器的時間
    current_time = datetime.utcnow()
    
    return TimeResponse(
        timestamp=current_time.timestamp(),
        iso_format=current_time.isoformat()
    )

@app.get("/")
async def read_root():
    return {"message": "NTP-like server is running"}

# 用 uvicorn 啟動 NTP 伺服器
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)