# HTML 處理與萃取

from bs4 import BeautifulSoup

def extract_relevant_html(raw_html: str, max_length: int = 3000) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    title = soup.title.string if soup.title else ""
    metas = [str(meta) for meta in soup.find_all("meta") if meta.get("name") in ["description", "keywords", "author"]]
    links = [a.get("href") for a in soup.find_all("a", href=True)[:10]]
    body_text = soup.get_text("\n", strip=True)[:1000]

    result = f"<title>{title}</title>\n{' '.join(metas)}\n<links>{links}</links>\n<body>{body_text}</body>"
    return result[:max_length]


# ------------------------------
# 功能：將完整 HTML 網頁內容萃取成簡化文本，方便送給分析模型處理。
# 使用套件：BeautifulSoup (pip install beautifulsoup4)

# 1. 解析 HTML：
#    - 將 raw_html 用 BeautifulSoup 解析成可操作的 HTML 結構。
#    - 'html.parser' 是內建解析器，無需額外安裝 lxml 等。

# 2. 提取主要欄位：
#    - title：網頁標題 (soup.title.string)
#    - meta：抓取 name 為 description、keywords、author 的 meta 標籤
#    - links：抓前 10 個 href，通常包含登入/註冊/購物車等重要連結
#    - body_text：抓正文文字，限制前 1000 字

# 3. 組合成簡化 HTML 字串：
#    - 形成格式：
#      <title>標題</title>
#      <meta 標籤列表>
#      <links>前 10 個連結</links>
#      <body>正文文字</body>
#    - 最後用 max_length 限制總長度，避免送給模型過大文字。

# 4. 使用場景：
#    - 將萃取後的簡化 HTML 傳給分析函式（analyze_web）進行釣魚網站判斷。
#    - 如果輸入不是 HTML，則可直接傳入純文字進行分析。
