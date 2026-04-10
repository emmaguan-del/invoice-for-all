# Gmail → 客服信紀錄 Sheet 同步腳本

## 目的
從 Gmail 抓取與 `support@invos.com.tw`、`invos_service@invos.com.tw` 相關的信件，去重後 append 到 Google Sheet：`客服信紀錄`。

## 目標 Sheet
- Spreadsheet ID: `1yDHP29PODaXAIt1xVQ5YunBF2wrDMkRNcD1-MZ9QVow`
- 工作表: `客服信紀錄`

## 功能
- 搜尋 Gmail 中 from / to 包含以下信箱的郵件：
  - `support@invos.com.tw`
  - `invos_service@invos.com.tw`
- 用 `messageId` / `threadId` 去重
- 自動寫入下列欄位：
  - 日期
  - 用戶暱稱
  - Email
  - 手機型號
  - 平台
  - APP版本
  - 載具號碼
  - 問題標籤
  - 問題摘要
  - 分類
  - 重要性
  - 是否回覆
  - 回覆時間
  - 狀態
  - messageId
  - threadId

## 先決條件
1. 安裝 Python 套件：
```bash
pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```

2. 將 Google OAuth client JSON 放在：
```bash
~/Downloads/client_secret.json
```
如果檔名不同，可直接修改 `gmail_to_customer_sheet.py` 裡的 `CREDS_PATH`。

## 第一次執行
```bash
python3 gmail_to_customer_sheet.py
```
第一次會自動開瀏覽器要求你登入 Google 並授權。

授權成功後會產生：
```bash
~/gmail_sheet_token.json
```

## 之後執行
```bash
python3 gmail_to_customer_sheet.py
```

## 注意
- 第一版 parser 先以穩定同步為主
- 若 Gmail 內文格式不一致，`手機型號 / APP版本 / 載具號碼 / 分類` 等欄位可能需要再迭代 parser
- `是否回覆`、`回覆時間` 目前預設留空
- `狀態` 預設寫入 `待處理`

## 建議下一步
- 加上只抓指定日期區間
- 加上只抓未同步的新信
- 強化 parser，針對既有客服信模板更準確抽欄位
- 加上自動判斷是否已回覆
