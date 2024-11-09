# 使用 Node.js 官方映像
FROM node:16

# 設定工作目錄
WORKDIR /app

# 複製前端應用程式代碼
COPY . .

# 安裝依賴並啟動應用
RUN npm install
CMD ["npm", "start"]
