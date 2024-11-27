# DB1131_final_project

2024/11/9 update

## 安裝 Docker & Docker-compose

上網裝

## Execution

把整個專案跑起來，執行

```bash
./run.sh
```

確認服務是否都有跑起來，執行

```bash
docker-compose ps
```
應該要看到三個服務（frontend, backend, db)

想要監控後端的輸出，在另一個終端機視窗執行

```bash
docker-compose logs -f backend
```

## Stop

停止整個專案（資料庫內容會存起來）

```bash
./stop.sh
```

## Clean

將資料庫內容清掉

```bash
./clean.sh
```

