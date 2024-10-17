#!/bin/bash

# 檢查 chronyd 是否在運行
if pgrep chronyd > /dev/null
then
    echo "chronyd is already running."
else
    echo "Starting chronyd..."
    chronyd
fi

# 啟動 FastAPI 伺服器
echo "Starting FastAPI server..."
uvicorn app:app --host 0.0.0.0 --port 5000