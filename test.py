# 基本測試模型判斷，你現在不會用到

import json
from html_utils import extract_relevant_html
from analyzer import analyze_web

text = """

<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <title>中華郵政 - 包裹待領通知</title>
</head>
<body>
  <h1>📦 包裹未領取通知</h1>
  <p>親愛的客戶，您的包裹因地址不完整而無法送達。</p>
  <p>請立即登入以下網站補充地址資訊，以避免包裹被退回：</p>
  <a href="http://post-tw-delivery-confirm.com/verify">http://post-tw-delivery-confirm.com/verify</a>
  <p>若 24 小時內未完成驗證，您的包裹將被退回寄件人。</p>
  <footer>
    客服信箱：support@post-service-help.com<br>
    © 2025 Chunghwa Post. All Rights Reserved.
  </footer>
</body>
</html>

"""

reduced_html = extract_relevant_html(text)
analysis = analyze_web(reduced_html)
print(json.dumps(analysis.model_dump(), indent=2, ensure_ascii=False))
