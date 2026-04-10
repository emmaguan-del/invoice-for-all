#!/usr/bin/env python3
import os
import re
import base64
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ===== Config =====
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
]

SHEET_ID = "1yDHP29PODaXAIt1xVQ5YunBF2wrDMkRNcD1-MZ9QVow"
SHEET_NAME = "客服信紀錄"
SENDERS = ["support@invos.com.tw", "invos_service@invos.com.tw"]
TOKEN_PATH = os.path.expanduser("~/gmail_sheet_token.json")
CREDS_PATH = os.path.expanduser("~/Downloads/client_secret.json")

HEADERS = [
    "日期",
    "用戶暱稱",
    "Email",
    "手機型號",
    "平台",
    "APP版本",
    "載具號碼",
    "問題標籤",
    "問題摘要",
    "分類",
    "重要性",
    "是否回覆",
    "回覆時間",
    "狀態",
    "messageId",
    "threadId",
]


def get_creds():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDS_PATH):
                raise FileNotFoundError(f"OAuth client JSON not found: {CREDS_PATH}")
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return creds


def gmail_query():
    terms = []
    for addr in SENDERS:
        terms.append(f"from:{addr}")
        terms.append(f"to:{addr}")
    return "{" + " OR ".join(terms) + "}"


def ensure_headers(sheet_service):
    result = sheet_service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=f"{SHEET_NAME}!A1:P2"
    ).execute()
    values = result.get("values", [])
    if not values:
        sheet_service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=f"{SHEET_NAME}!A1:P1",
            valueInputOption="USER_ENTERED",
            body={"values": [HEADERS]},
        ).execute()


def get_existing_ids(sheet_service):
    result = sheet_service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=f"{SHEET_NAME}!O:P"
    ).execute()
    values = result.get("values", [])
    existing_msg_ids = set()
    existing_thread_ids = set()
    for row in values[1:]:
        if len(row) > 0 and row[0]:
            existing_msg_ids.add(row[0].strip())
        if len(row) > 1 and row[1]:
            existing_thread_ids.add(row[1].strip())
    return existing_msg_ids, existing_thread_ids


def decode_body(payload):
    if not payload:
        return ""
    body = payload.get("body", {})
    data = body.get("data")
    if data:
        return base64.urlsafe_b64decode(data.encode("UTF-8")).decode("utf-8", errors="ignore")
    for part in payload.get("parts", []):
        mime = part.get("mimeType", "")
        if mime in ("text/plain", "text/html"):
            text = decode_body(part)
            if text:
                return text
    return ""


def extract_header(headers, name):
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def parse_sender_name_and_email(from_value):
    m = re.search(r'^(.*?)\s*<([^>]+)>$', from_value)
    if m:
        return m.group(1).strip().strip('"'), m.group(2).strip()
    if "@" in from_value:
        return "", from_value.strip()
    return from_value.strip(), ""


def parse_date(date_str):
    try:
        dt = parsedate_to_datetime(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone().strftime("%Y-%m-%d %H:%M")
    except Exception:
        return date_str


def infer_platform(text, subject):
    source = f"{subject}\n{text}".lower()
    if "iphone" in source or "ios" in source:
        return "iOS"
    if "android" in source or "pixel" in source or "samsung" in source or "oppo" in source or "xiaomi" in source or "vivo" in source:
        return "Android"
    return ""


def extract_device(text):
    patterns = [
        r"(iPhone[\w, ]+)",
        r"(Google Pixel[\w, ]+)",
        r"(Samsung[\w\- ]+)",
        r"(OPPO[\w\- ]+)",
        r"(Xiaomi[\w\- ]+)",
        r"(Vivo[\w\- ]+)",
        r"(裝置ID[:：].*)",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return ""


def extract_app_version(text):
    m = re.search(r"(?:APP版本|版本|iOS|Android)\s*[:：]?\s*([0-9]+(?:\.[0-9]+){1,3})", text, re.IGNORECASE)
    return m.group(1).strip() if m else ""


def extract_carrier_code(text):
    m = re.search(r"(/[A-Z0-9+\-.]{7,8})", text)
    return m.group(1).strip() if m else ""


def classify_issue(subject, body):
    source = f"{subject}\n{body}".lower()
    if any(k in source for k in ["刪除", "刪帳", "delete account", "帳號刪除"]):
        if any(k in source for k in ["廣告", "ad"]):
            return "帳號刪除", "刪帳-廣告太多", "高"
        if any(k in source for k in ["換號碼", "換手機號碼", "換電話", "新號碼"]):
            return "帳號刪除", "刪帳-換號碼", "中"
        if any(k in source for k in ["信箱", "email", "帳號"]):
            return "帳號刪除", "刪帳-換帳號/信箱", "中"
        if any(k in source for k in ["不用", "不使用", "不再使用", "用不到", "停止使用", "暫時不需要"]):
            return "帳號刪除", "刪帳-不再使用", "中"
        if any(k in source for k in ["不好用", "不美觀"]):
            return "帳號刪除", "刪帳-不好用", "高"
        return "帳號刪除", "刪帳-無說明", "中"
    if any(k in source for k in ["活動", "event", "campaign"]):
        return "活動問題", "活動問題", "低"
    return "待分類", "待分類", "中"


def summarize(subject, body):
    clean = re.sub(r"\s+", " ", body).strip()
    if subject and clean:
        return f"{subject} {clean[:80]}"[:120]
    if subject:
        return subject[:120]
    return clean[:120]


def fetch_all_messages(gmail_service):
    q = gmail_query()
    all_msgs = []
    page_token = None
    while True:
        resp = gmail_service.users().messages().list(
            userId="me",
            q=q,
            maxResults=500,
            pageToken=page_token,
        ).execute()
        all_msgs.extend(resp.get("messages", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return all_msgs


def main():
    creds = get_creds()
    gmail_service = build("gmail", "v1", credentials=creds)
    sheet_service = build("sheets", "v4", credentials=creds)

    ensure_headers(sheet_service)
    existing_msg_ids, existing_thread_ids = get_existing_ids(sheet_service)

    messages = fetch_all_messages(gmail_service)
    print(f"Found {len(messages)} matched Gmail messages")

    rows_to_append = []
    for msg_ref in messages:
        full = gmail_service.users().messages().get(userId="me", id=msg_ref["id"], format="full").execute()
        msg_id = full.get("id", "")
        thread_id = full.get("threadId", "")
        if msg_id in existing_msg_ids or thread_id in existing_thread_ids:
            continue

        payload = full.get("payload", {})
        headers = payload.get("headers", [])
        subject = extract_header(headers, "Subject")
        from_value = extract_header(headers, "From")
        date_value = extract_header(headers, "Date")
        internal_date = full.get("internalDate")

        body = decode_body(payload)
        nickname, email = parse_sender_name_and_email(from_value)
        parsed = parse_date(date_value)
        if not parsed and internal_date:
            parsed = datetime.fromtimestamp(int(internal_date)/1000).strftime("%Y-%m-%d %H:%M")

        device = extract_device(body)
        platform = infer_platform(body, subject)
        app_version = extract_app_version(body)
        carrier_code = extract_carrier_code(body)
        category, tag, priority = classify_issue(subject, body)
        summary = summarize(subject, body)

        row = [
            parsed,
            nickname,
            email,
            device,
            platform,
            app_version,
            carrier_code,
            category,
            summary,
            tag,
            priority,
            "",
            "",
            "待處理",
            msg_id,
            thread_id,
        ]
        rows_to_append.append(row)

    if not rows_to_append:
        print("No new rows to append")
        return

    sheet_service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=f"{SHEET_NAME}!A:P",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": rows_to_append},
    ).execute()

    print(f"Appended {len(rows_to_append)} new rows to {SHEET_NAME}")


if __name__ == "__main__":
    main()
