FROM python:3.12.0-slim

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# 暴露 5000 端口
EXPOSE 5000

# 使用腳本啟動 chronyd 和 FastAPI
CMD uvicorn app:app --host 0.0.0.0 --port 5000
