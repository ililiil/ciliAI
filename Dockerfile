# 前端构建阶段
FROM node:16-alpine as frontend
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 后端运行阶段
FROM python:3.9-slim
WORKDIR /app
COPY --from=frontend /app/dist ./static
COPY app.py .
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 5001
CMD ["python", "app.py"]