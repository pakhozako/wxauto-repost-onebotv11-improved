FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libx11-6 \
    libxcb1 \
    libxext6 \
    libxrender1 \
    libxi6 \
    libxtst6 \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY . .

# 创建配置目录
RUN mkdir -p config cache/images cache/files cache/voices logs

# 暴露端口
EXPOSE 10001

# 启动命令
CMD ["python", "main.py"]
