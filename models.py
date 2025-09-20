# Pydantic 模型

from pydantic import BaseModel, Field
from enum import Enum
from typing import List

class PhishingProbability(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class SuspiciousElement(BaseModel):
    element: str = Field(..., description="可疑元素名稱（請用繁體中文）")
    reason: str = Field(..., description="原因（請用繁體中文）")

class SimplePhishingAnalysis(BaseModel):
    is_potential_phishing: bool
    phishing_probability: PhishingProbability
    suspicious_elements: List[SuspiciousElement]
    recommended_actions: List[str] = Field(..., description="建議行動（請用繁體中文）")
    explanation: str = Field(..., description="總體說明（請用繁體中文）")

# ------------------------------
# 功能：定義分析釣魚網站或可疑內容的 JSON 結構
# 使用套件：
#   - pydantic (pip install pydantic)

# 1. PhishingProbability (Enum)
#    - 釣魚風險等級：
#        * LOW    : 低
#        * MEDIUM : 中
#        * HIGH   : 高

# 2. SuspiciousElement (Pydantic Model)
#    - 表示單一可疑元素：
#        * element : 可疑元素名稱（例如：網址、寄件者信箱、標題）
#        * reason  : 為何判定為可疑（中文描述原因）

# 3. SimplePhishingAnalysis (Pydantic Model)
#    - 整體分析結果：
#        * is_potential_phishing : 是否可能為釣魚 (bool)
#        * phishing_probability  : 釣魚風險等級 (PhishingProbability)
#        * suspicious_elements   : 可疑元素列表 (List[SuspiciousElement])
#        * recommended_actions   : 建議使用者採取的行動 (List[str])
#        * explanation           : 總體說明 (str)
