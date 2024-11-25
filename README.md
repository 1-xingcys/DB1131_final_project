# DB1131_final_project

2024/11/25 update by 1xing

* 新增前端程式碼註解，從 `App.js` 開始看才看的懂
* 更改後端程式的檔案架構，如群組所述
* 新增 `customerApi.py` 裡面定義所有 customer 使用者會用到的 api，目前包含昨天討論做的 `/restaurant/info/regular` 和剛剛我自己新增的 `/customer/cname`
  *  `/customer/cname` api，讓使用者用 id, passwd 登入之後，前端能知道使用者的 name。
* 更改整個專案的執行方式：
  * `./run.sh all` 執行前後端跟資料庫，作為整體測試用
  * `./run.sh dev` 只執行後端跟資料庫，可以單純用 postman 測試 API 的功能，或是讓前端在本地跑（在 frontend 資料夾執行 `npm start`）以使用 live server 功能（網頁畫面即時隨程式碼更改產生變化）

## Execution

把整個專案跑起來，執行

```bash
./run.sh all
```

只跑後端跟資料庫，執行

```bash
./run.sh dev
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

