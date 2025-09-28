# 呼叫本地端 API 分析

from models import SimplePhishingAnalysis
from openai import OpenAI
import instructor

#  Ollama 模型名稱
OLLAMA_MODEL = "gemma3:12b"

# 創建 client
client = instructor.from_openai(
    OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama"),
    mode=instructor.Mode.JSON,
)

def analyze_web(content: str) -> SimplePhishingAnalysis:
    messages = [
        {
            "role": "system",
            "content": (
                "你是一個資安專家 AI 助手，專門分析網頁詐騙與釣魚網站。"
                "所有輸出必須完全使用繁體中文，禁止任何英文。"
                "輸出必須符合 SimplePhishingAnalysis 模型的 JSON 結構。"
                "除非有明顯且多重釣魚特徵，否則標記為 Likely Legitimate。"
                "遇到知名教育機構或政府單位網站，預設為合法，除非網址或內容有明顯異常。"
                "如果輸入中包含 <extracted_urls> 區塊，請逐項檢視清單中的每個網址是否疑似假冒、拼字相近、可疑子網域、短網址轉跳、HTTP 非加密、異常 TLD、或與頁面主��無關等；並將觀察到的可疑元素與建議動作寫入對應欄位。"
            ),
        },
        {
            "role": "user",
            "content": content,
        },
    ]

    resp = client.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=messages,
        response_model=SimplePhishingAnalysis,
    )
    return resp

# ------------------------------
# 功能：使用本地 Ollama 模型 (gemma3:12b) 分析 HTML 或純文字，判斷釣魚網站風險。
# 使用套件：
#   - instructor (pip install instructor)
#   - openai (pip install openai)
#   - models.py 裡的 SimplePhishingAnalysis

# 1. 設定模型名稱：
#    - OLLAMA_MODEL = "gemma3:12b"
#    - 此模型為本地部署的 JSON 指令模型，分析約需 30 秒。

# 2. 創建 client：
#    - 使用 instructor.from_openai 將本地 Ollama OpenAI API 包裝為 JSON 模式。
#    - base_url 指向本地 Ollama 伺服器 (127.0.0.1:11434)。
#    - mode=instructor.Mode.JSON 強制返回 JSON 格式，方便與 Pydantic 模型匹配。

# 3. analyze_web(content: str) 函式：
#    - messages：
#        * system：告訴模型你是資安專家，輸出必須符合 SimplePhishingAnalysis 結構。
#        * user：將要分析的 HTML 或純文字內容。
#    - 呼叫 client.chat.completions.create()：
#        * model：選定 Ollama 模型
#        * messages：輸入訊息
#        * response_model：指定回傳 JSON 對應的 Pydantic 模型
#    - 回傳 resp：SimplePhishingAnalysis 型態，包含：
#        * is_potential_phishing (bool)
#        * phishing_probability (low/medium/high)
#        * suspicious_elements (可疑元素列表)
#        * recommended_actions (建議行動)
#        * explanation (總體說明)
