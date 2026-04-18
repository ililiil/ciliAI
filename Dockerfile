# 前端构建阶段
FROM node:20-alpine AS frontend
WORKDIR /app

RUN npm config set registry https://registry.npmmirror.com

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 后端运行阶段
FROM python:3.9-slim
WORKDIR /app

# 安装 curl 用于健康检查
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/uploads && chmod 755 /app/uploads

# 复制前端构建产物
COPY --from=frontend /app/dist ./dist

# 复制后端代码
COPY app.py .
COPY key_manager.py .
COPY db_manager.py .
COPY init_mysql_db.py .
COPY requirements.txt .

# 配置pip使用国内镜像源并安装依赖
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir -r requirements.txt --timeout 120 --retries 5

# 复制.env文件
COPY .env /app/.env

EXPOSE 5001

# 启动命令：先初始化数据库，再启动应用
CMD ["sh", "-c", "python init_mysql_db.py && python app.py"]
