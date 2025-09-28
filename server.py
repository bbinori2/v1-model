# 用 Flask Server 來接收文字/HTML

from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import analyze_web
from html_utils import extract_relevant_html, extract_urls

app = Flask(__name__)
CORS(app)  # 允許所有來源跨域請求

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")

    # 先從輸入中抓取網址，供模型審查
    urls = extract_urls(text)

    if "<html" in text.lower():
        reduced_html = extract_relevant_html(text)
    else:
        reduced_html = text

    # 將擷取網址以特殊區塊附加，讓模型可針對清單逐一審視
    if urls:
        urls_block = "<extracted_urls>\n" + "\n".join(urls[:50]) + "\n</extracted_urls>"
        reduced_html = f"{reduced_html}\n\n{urls_block}"

    analysis = analyze_web(reduced_html)
    return jsonify(analysis.model_dump())

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

# ------------------------------
# 功能：建立本地 HTTP API，接收 POST 請求，傳入文字或 HTML，回傳分析結果
# 使用套件：
#   - flask        (pip install flask)
#   - flask_cors   (pip install flask-cors)

# 1. Flask App 初始化
#    - app = Flask(__name__) ：建立 Flask 應用
#    - CORS(app)             ：允許所有來源跨域請求（Extension 或其他前端可以呼叫）

# 2. /analyze 路由 (POST)
#    - 接收 JSON 內容：{ "text": "要分析的文字或 HTML" }
#    - 判斷是否 HTML：
#        * 如果包含 "<html" 則使用 extract_relevant_html() 萃取重要內容
#        * 否則直接使用純文字
#    - 呼叫 analyze_web() 進行分析，回傳 Pydantic 模型結果
#    - 使用 jsonify() 將結果轉成 JSON 回應

# 3. 啟動 Server
#    - host="127.0.0.1", port=5000
#    - debug=True 方便開發時自動重載與除錯
    
# 4. 使用方式：
#    - 前端或 Extension 可 POST 到 http://127.0.0.1:5000/analyze
#    - 內容可以是 HTML 或純文字
#    - 回傳 JSON 格式符合 SimplePhishingAnalysis
