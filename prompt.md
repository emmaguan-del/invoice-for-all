請修改 public/index.html，針對以下 user story 重新設計 UX 文案與流程：

## User Story
我是來台灣旅遊/工作的外國人，不懂中文，也完全不知道「載具」「歸戶」這些專有名詞是什麼意思。但我聽說台灣發票可以抽獎中現金，我想試試看。

## 核心原則
1. 預設語言改為英文（EN 為主，保留語言切換）
2. 零術語：所有中文專有名詞要替換成外國人能理解的說法
3. 教學式 UX：每個步驟解釋「為什麼」，不只是「做什麼」
4. 降低登入門檻：外國人通常沒有手機條碼，要讓 Google 登入變成最主要的入口

## 具體修改項目

### 登入頁重新設計
廢掉「我有手機條碼（電子載具）」這個說法，改成：

次要選項（右上小連結）："Already have a barcode? Link it"
主要入口：
- 大標題："Scan receipts. Win cash prizes."
- 副標題："Taiwan government runs a national lottery — every receipt is a chance to win up to NT$10,000,000!"
- 主要按鈕（大）：Continue with Google
- 次要按鈕：Continue with Facebook / Continue with LINE
- 最底部：Skip for now

### 術語替換（全局）
- 載具 → Receipt Wallet / your barcode
- 歸戶 → Linked to your account
- 手機條碼 → Mobile barcode (receipt wallet)
- 對獎 → Check prizes / Lottery check
- 開獎 → Prize draw
- 中獎 → You won!
- 未中獎 → No prize this time
- 待對獎 → Not checked yet
- 捐贈 → Donate prize
- 發票 → Receipt (invoice)
- 期別 → Period
- 歸戶發票 → Linked receipts

### 首頁 Header
- 問候語："Hi! Ready to win?"
- 說明："You have 12 receipts to check for prizes"
- 統計：Receipts: 23 / Coins: 450 / Vouchers: 2

### 掃描頁
掃描框上方加說明："Scan the barcode or QR code on your receipt"
掃描成功明細卡片：
- 標題："Receipt saved!"
- 副標題："We'll check this in the next prize draw"

### 發票列表頁
- 標題："My Receipts"
- 篩選 chip：All / Unchecked / Won! / No prize / Donated
- 狀態 badge：Pending（灰）/ Won NT$200（金色）/ No prize（淡灰）

### Wallet Tab（原「載具」）
- Tab 名稱：Wallet
- 頁面標題："Receipt Barcode Wallet"
- 說明："Show this barcode at checkout to automatically collect receipts"
- 條碼說明："Your unique government-issued barcode"

### 帳戶頁對獎功能
- 卡片標題："Prize Lottery"
- 說明："Taiwan government holds a bi-monthly prize draw. Check if your receipts won!"
- 期別："Jan-Feb 2026 Draw"
- 按鈕："Check My Prizes"

對獎 Modal：
- 掃描中："Checking your receipts..."
- 結果標題：中獎 "Congratulations!" / 沒中 "Better luck next time!"
- 中獎說明："2 of your receipts won prizes totaling NT$400"
- 中獎卡片底部加："How to claim your prize" 小連結

### 加入 What is this? 說明頁（問號 icon 點開）
3 步驟卡片：
1. Every receipt in Taiwan is a lottery ticket
2. Scan to save and track your receipts
3. Check prizes every 2 months (government draw)
4. Win up to NT$10,000,000!

Prize table：
- Special Prize: NT$10,000,000
- Grand Prize: NT$2,000,000
- First Prize: NT$200,000
- Second Prize: NT$40,000
- Third Prize: NT$10,000
- Fourth Prize: NT$2,000
- Fifth Prize: NT$1,000
- Sixth Prize: NT$200

## 保留
- 所有動畫效果不變
- Tab Bar 5個 tab 不變
- 掃描、對獎動畫不變
- 設計系統顏色字型不變

修改完成後把 public/index.html 存好。

完成後執行：
openclaw system event --text "Done: 外國人友善版 prototype 完成，請 deploy" --mode now
