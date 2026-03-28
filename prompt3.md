請修改 public/index.html，把首頁（homePage）內所有硬碼的中文文字，改成透過 i18n 系統動態渲染，讓語言切換時整頁一致。

## 需要修正的區塊

### 1. 發票統計卡片（stats-card）

目前是硬碼中文，要改成 i18n。

找到這段結構，把文字都改成 data-i18n 或用 JS 渲染：
- "張發票已存入" → i18n key: statInvoicesLabel
- "再存入 7 張，本期中獎機率可望提升 15% ↑" → i18n key: statBoostHint（含 HTML 格式）
- "本期進度 23 / 30 張" → i18n key: statProgress

zh-TW 值：
- statInvoicesLabel: "張發票已存入"
- statBoostHint: '再存入 <b style="color:var(--blue)">7 張</b>，本期中獎機率可望提升 <b style="color:var(--blue)">15%</b> ↑'
- statProgress: "本期進度 23 / 30 張"

en 值：
- statInvoicesLabel: "receipts saved"
- statBoostHint: 'Save <b style="color:var(--blue)">7 more</b> to boost your prize odds by <b style="color:var(--blue)">15%</b> ↑'
- statProgress: "This period: 23 / 30 receipts"

### 2. 載具條碼區塊

未設定狀態：
- "手機載具條碼" → key: carrierTitle（zh: 手機載具條碼 / en: Receipt Barcode Wallet）
- "中獎機率 +3倍" → key: carrierBoostBadge（zh: 中獎機率 +3倍 / en: 3x prize odds）
- "點此設定載具條碼" → key: carrierSetupCTA（zh: 點此設定載具條碼 / en: Set up your barcode wallet）
- "設定後可直接在這裡顯示" → key: carrierSetupSub（zh: 設定後可直接在這裡顯示 / en: It will appear here after setup）

已設定狀態：
- "手機載具條碼" → 同 carrierTitle
- "全螢幕 ↗" → key: carrierFullscreen（zh: 全螢幕 ↗ / en: Fullscreen ↗）
- "發票存摺 手機條碼：/ABC-1234" → key: carrierBarcodeLabel（zh: 發票存摺 手機條碼：/ABC-1234 / en: Receipt Wallet Barcode: /ABC-1234）

### 3. 消費分析右側代辦清單

- "🎯 提升中獎機率" → key: todoTitle（zh: 🎯 提升中獎機率 / en: 🎯 Boost Your Prize Odds）
- "綁定銀行帳號" → key: todoBankTitle（zh: 綁定銀行帳號 / en: Link Bank Account）
- "中獎可直接入帳 +方便" → key: todoBankSub（zh: 中獎可直接入帳 <b>+方便</b> / en: Receive prize money directly）
- "稍後設定"（兩個按鈕都一樣）→ key: todoLater（zh: 稍後設定 / en: Set up later）
- "載具歸戶" → key: todoCarrierTitle（zh: 載具歸戶 / en: Link Cloud Receipts）
- "雲端發票獎 +2次機會" → key: todoCarrierSub（zh: 雲端發票獎 <b>+2次機會</b> / en: Cloud receipt lottery <b>+2 chances</b>）

### 4. 發票明細 modal（showInvoiceDetail 函數）

把 modal 裡的中文標籤改成 i18n：
- "電子發票證明聯" → key: detailHeader（zh: 電子發票證明聯 / en: Electronic Invoice）
- "隨機碼：" → key: detailRandom（zh: 隨機碼： / en: Random Code:）
- "開立日期" → key: detailDate（zh: 開立日期 / en: Date）
- "店家" → key: detailShop（zh: 店家 / en: Store）
- "地址" → key: detailAddress（zh: 地址 / en: Address）
- "對獎狀態" → key: detailStatus（zh: 對獎狀態 / en: Prize Status）
- "消費明細" → key: detailItems（zh: 消費明細 / en: Items）
- "合計" → key: detailTotal（zh: 合計 / en: Total）
- "財政部電子發票" → key: detailFooter1（zh: 財政部電子發票 / en: Taiwan Government E-Invoice）
- "本發票已存入你的發票存摺帳戶" → key: detailFooter2（zh: 本發票已存入你的發票存摺帳戶 / en: Saved to your Receipt Wallet）
- "開獎日：115年3月25日" → key: detailFooter3（zh: 開獎日：115年3月25日 / en: Prize draw date: Mar 25, 2026）
- 中獎 banner "恭喜！這張發票中獎" → key: detailWonTitle（zh: 恭喜！這張發票中獎 / en: Congratulations! This receipt won!）
- "獎金 NT$X 元，請至郵局兌領" → 動態但文字部分 key: detailWonSub（zh: 獎金 NT$${prize} 元，請至郵局兌領 / en: You won NT$${prize}! Claim at any post office）
- 捐贈 banner "此發票已捐贈" → key: detailDonatedTitle（zh: 此發票已捐贈 / en: Donated）
- "發票明細" 標題 → key: detailModalTitle（zh: 發票明細 / en: Receipt Details）

## 實作方式

1. 在 i18n 物件的 'zh-TW' 和 'en' 裡加入上述所有 key
2. HTML 裡的靜態文字用 data-i18n attribute 或在 applyI18n() 裡用 JS 更新 innerHTML
3. showInvoiceDetail() 裡的文字改用 t('key') 函數取值
4. 確保語言切換後，這些區塊也會即時更新（包含已開啟的 modal）

## 注意
- 不要改動任何功能邏輯
- 不要改動 CSS 樣式
- 只修改文字的語言對應

完成後儲存 public/index.html。

完成後執行：
openclaw system event --text "Done: 首頁 i18n 統一完成，請 deploy" --mode now
