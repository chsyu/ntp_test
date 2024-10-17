FROM python:3.12.0-slim

WORKDIR /code

RUN apt-get update && apt-get install -y chrony procps

RUN mkdir -p /etc/chrony
COPY chrony.conf /etc/chrony/chrony.conf

# 複製啟動腳本
COPY start.sh /start.sh
RUN chmod +x /start.sh  # 賦予腳本執行權限

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# 暴露 5000 端口
EXPOSE 5000

# 使用腳本啟動 chronyd 和 FastAPI
CMD ["/start.sh"]
