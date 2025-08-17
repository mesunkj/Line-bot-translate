# LineBot-VI-CHN-Translator

本專案是一個 LINE Bot，支援中文（繁體）與越南語的自動雙向翻譯，並可處理長文本。Bot 以 Flask 架設，結合 LINE Messaging API 與 Google Translate，適合教學、語言交流等場景。

## 功能特色

- 支援 LINE Bot 雙向中文/越南語翻譯
- 長文本自動分段翻譯
- 語言自動偵測
- 非同步翻譯流程，效能佳
- 內建測試劇本驗證翻譯品質

## 快速開始

1. 安裝依賴套件
    ```sh
    pip install -r requirements.txt
    ```

2. 設定 LINE Channel access token 與 secret，填入 `line_bot_server translate 0.01x.py`。

3. 啟動 Flask 伺服器
    ```sh
    python "line_bot_server translate 0.01x.py"
    ```

4. 使用 ngrok 取得公開網址，設定 webhook 至 LINE Developer 平台。

## 主要檔案

- [`line_bot_server translate 0.01x.py`](line_bot_server%20translate%200.01x.py)：LINE Bot 主伺服器
- [`translate_vi_chn.py`](translate_vi_chn.py)：翻譯核心模組
- [`requirements.txt`](requirements.txt)：依賴套件清單

## 參考

- [LINE Messaging API 官方文件](https://developers.line.biz/console/channel/2007800550/messaging-api)
- [Googletrans](https://pypi.org/project/googletrans/)
- [ngrok](https://steam.oxxostudio.tw/category/python/example/ngrok.html)

---

如需協助或回報問題，請
