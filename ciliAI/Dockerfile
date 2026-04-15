# 前端构建阶段
FROM node:20-alpine as frontend
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 后端运行阶段
FROM python:3.9-slim
WORKDIR /app
RUN mkdir -p /app/uploads && chmod 755 /app/uploads
COPY --from=frontend /app/dist ./dist
COPY app.py .
COPY key_manager.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001
CMD ["python", "app.py"]