# DB1131_final_project

## Prerequisite

我們的系統是用 docker 容器化技術來打包，執行的主機需事先安裝好 `docker` 引擎和 `docker-compose`。另外，我們的前端、後端、資料庫服務分別會轉發到主機的 `3000`、`5001`、 `5433` ports，確認主機的這幾個 ports 沒有其它服務正在跑以避免不預期的情況發生。

## Execution

在專案主目錄下用以下 script 來執行系統，第一次 build 可能需要一段時間

```bash
./run.sh all
```

確認服務是否都有跑起來，執行

```bash
docker-compose ps
```
應該要看到三個服務（frontend, backend, db) 以及其資訊

## Logs

在另一個終端機視窗執行，監控後端的輸出

```bash
docker-compose logs -f backend
```

在另一個終端機視窗執行，監控資料庫 server 的輸出

```bash
docker-compose logs -f db
```

## Connect to the system

打開瀏覽器輸入以下網址，連接前端服務

```
http://localhost:3000
```

若有需要，也可以自行連接後端、資料庫服務

## Stop

停止整個專案

```bash
./stop.sh
```