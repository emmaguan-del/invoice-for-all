# 新使用者 Onboarding Storyboard（依 source code 重建）

## 文件目的
根據 iOS / Android source code，重建「新註冊使用者從首次開啟 App，到完成 onboarding 並進入主系統」的逐畫面 storyboard，並補充失敗分支，作為產品、設計與需求討論依據。

> 主要依據：
> - Android：`LoginIndexScreen`、`LinkCarrierScreen`、`OneTimePasswordFragment`、`CarrierLoginScreen`、`LoginContainerActivity`、`LoginViewModel`
> - iOS：`LoginVC`、`LinkCarrierVC`、`OneTimePasswordVerifyViewController`、`CarrierLoginViewController`

---

# 一、主線 Storyboard

## Screen 01｜登入首頁 / 入口選擇

### 畫面目的
讓使用者先決定：
- 我已經有載具 → 登入
- 我還沒有 → 註冊

### 畫面構圖
- 上半部：大張品牌背景圖
- 下半部：白色圓角底板
- 中間 slogan
- 下方兩顆主按鈕
- 最底部條款 checkbox

### 畫面元素
- Slogan / login slogan
- Primary CTA：**載具登入**
- Secondary CTA：**註冊載具與會員**
- Checkbox：**我同意使用者條款與隱私權政策**
- 條款文字可點

### 使用者操作
- 新手通常點：**註冊載具與會員**
- 若未勾選條款，會跳 agreement dialog

---

## Screen 02｜條款確認 Dialog

### 出現條件
- 使用者尚未勾選條款，但想往下走

### 畫面型態
- 中央 modal dialog
- 背景頁面變暗

### 畫面元素
- 提醒需同意條款
- `同意`
- `不同意`
- 條款連結

### 使用者操作
- 點 **同意** → 回主流程
- 點 **不同意** → 停留 / 返回

---

## Screen 03｜載具必要性說明頁

### 畫面目的
教育新使用者為什麼需要先有載具，才能完整使用 App。

### 畫面構圖
- 上方 app bar
- 中間一張載具插圖
- 下方 benefit list
- 底部雙按鈕

### 畫面元素
- Header
- 右上角：`登出`
- 載具插圖
- 大標題
- 4 條 benefit
- Primary CTA：**已有載具，立即綁定**
- Secondary CTA：**註冊新載具**

### 使用者操作
- 新手通常點：**註冊新載具**

---

## Screen 04｜財政部註冊流程（App 內 WebView）

### 畫面目的
導入財政部 / MOF 的申請流程，完成手機條碼 / 載具註冊。

### 畫面構圖
- 上方仍是 app navigation bar
- 內容區切成官方 webview
- 畫面語氣從品牌 app 轉成官方表單

### 畫面元素
- 標題：類似 `手機條碼申請` / `註冊載具`
- 內嵌官方表單
- 驗證步驟
- 下一步 / 送出按鈕

### 使用者操作
- 填寫資料
- 完成財政部流程

### 重點
這不是純 app 原生頁，而是 **Hybrid onboarding**。

---

## Screen 05｜一次性驗證碼 OTP 頁

### 畫面目的
完成身分驗證，確認新註冊使用者可登入。

### 畫面構圖
- 上方返回列
- 中上區 OTP 欄位
- 中間說明文案
- 下方送出按鈕
- 底部倒數與 resend

### 畫面元素
- 標題：**一次性驗證碼**
- OTP input
- 提示文字：驗證碼已送至哪個手機
- 按鈕：**送出**
- 倒數計時
- 按鈕：**重新發送驗證碼**

### 使用者操作
- 輸入 OTP
- 點送出

---

## Screen 06A｜OTP 成功，且已取得 barcode

### 出現條件
- OTP 驗證成功
- 系統判定已有 carrier barcode

### 結果
- 不額外顯示完成頁
- 直接進主系統

---

## Screen 06B｜OTP 成功，但尚未取得 barcode

### 出現條件
- OTP 驗證成功
- 系統判定 `hasBarCode == false`

### 結果
- 不直接進主畫面
- 再導回補走載具申請 / 綁定流程

### 使用者感受
- 容易產生「我明明驗證成功了，怎麼還沒完成」的落差

---

## Screen 07｜進入主系統

### 畫面目的
代表 onboarding 真正完成。

### 使用者看到的內容（依 code 推估）
- 發票相關主頁
- 載具條碼
- 發票列表
- 主功能 tab

---

# 二、主線流程總結

1. 登入首頁
2. 條款確認
3. 載具必要性說明
4. 財政部 WebView 註冊
5. OTP 驗證
6. 檢查是否已有 barcode
7. 進主畫面（或補跑載具流程後再進）

---

# 三、失敗分支 Storyboard

## Failure 01｜未勾選條款就想繼續

### 觸發點
- 在登入首頁點擊 `載具登入` 或 `註冊載具與會員`
- 但 checkbox 未勾選

### 使用者看到什麼
- Agreement confirmation dialog 跳出
- 提醒需先同意使用者條款與隱私權政策

### 可做操作
- `同意`
- `不同意`
- 點開條款

### 可能結果
- 同意 → 回主流程
- 不同意 → 停留在登入入口

---

## Failure 02｜OTP 未填 / 空值送出

### 觸發點
- OTP 頁直接按送出，但沒有輸入驗證碼

### 使用者看到什麼
- OTP 欄位出錯
- 顯示必填錯誤訊息

### 使用者感受
- 這是最基本的表單錯誤阻擋

---

## Failure 03｜OTP 驗證失敗

### 觸發點
- 輸入錯誤驗證碼
- 或驗證碼過期

### 使用者看到什麼
- Snackbar / error message
- 留在 OTP 頁
- 可重新輸入

### 使用者下一步
- 重輸 OTP
- 若收不到或失效，等待後重發

---

## Failure 04｜收不到 OTP，需要重發

### 觸發點
- 使用者遲遲沒收到驗證碼

### 使用者看到什麼
- resend 按鈕初始不可用
- 倒數結束後可按 `重新發送驗證碼`

### 使用者操作
- 點 resend
- 系統重新發送 OTP
- UI 顯示已重送提示

### 風險
- 如果簡訊 / email 流程不順，這裡會是高流失點

---

## Failure 05｜OTP 成功，但其實沒有 barcode

### 觸發點
- OTP 驗證成功
- 系統判定尚未擁有 barcode

### 使用者看到什麼
- 不會直接進主畫面
- 會再被導去補走載具申請 / 綁定流程

### 使用者感受
- 認知落差最大
- 容易以為系統壞掉或流程重複

### 產品意義
- OTP 成功 ≠ onboarding 成功
- 真正完成條件是「拿到可用載具 / barcode」

---

## Failure 06｜已有帳號但載具未註冊 / 無法直接登入

### 觸發點
- 使用者走載具登入
- 但系統回傳 `CARRIER_NOT_REGISTERED` 或類似狀態

### 使用者看到什麼
- App 會導向 MOF login / signup / link carrier fallback flow
- 可能跳入官方 WebView

### 使用者感受
- 以為自己能直接登入，結果被要求補官方流程

---

## Failure 07｜忘記驗證碼

### 觸發點
- 在載具登入頁點 `忘記驗證碼`

### 使用者看到什麼
- 不是純原生處理，很可能開 MOF web flow
- 透過 `forgotPasswordUrl` / `MofWebLoginActivity` 補官方流程

### 使用者感受
- 需要回到官方處理，體驗不連續

### 產品意義
- 這是 onboarding 後、回流登入階段的重要 fallback

---

## Failure 08｜財政部 WebView 流程中斷或失敗

### 觸發點
- WebView 載入失敗
- 官方流程失敗
- 中途返回 / 取消

### 使用者看到什麼
- 回到 app flow
- 可能收到錯誤 snackbar / 提示
- 無法完成註冊或綁定

### 風險
- Hybrid flow 最大風險點
- 也是最可能導致使用者放棄 onboarding 的地方

---

# 四、這段 onboarding 的核心 friction

## 1. 條款勾選在前
還沒開始前就要求合規，會增加第一步阻力。

## 2. 註冊流程切進官方 WebView
體驗從品牌 app 突然切換成官方表單，心理落差大。

## 3. OTP 成功不一定代表完成
若還沒有 barcode，還要補流程，容易造成認知斷裂。

## 4. 忘記驗證碼與部分 fallback 依賴 MOF web
這表示註冊與登入雖然有 app 引導，但並非完全自洽閉環。

---

# 五、一句話結論

這套 onboarding 是一條 **品牌入口 → 載具教育 → 官方註冊 WebView → OTP 驗證 → barcode 檢查 → 進主系統** 的 hybrid flow；主要失敗點集中在條款、官方 WebView、OTP，以及「驗證成功但尚未真正取得 barcode」這幾個環節。
