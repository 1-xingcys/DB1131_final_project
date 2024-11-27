# 使用 Node.js 官方輕量級映像
FROM node:16-alpine

# 設定工作目錄
WORKDIR /app

# 複製依賴文件
COPY package.json package-lock.json ./

# 安裝依賴
RUN npm install

# 複製其餘前端代碼
COPY . .

# 啟動應用
CMD ["npm", "start"]
