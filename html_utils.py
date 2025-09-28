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


def _normalize_url(url: str) -> str | None:
    """標準化 URL，過濾無效協定與雜訊符號。
    - 移除結尾雜訊字元，例如引號、逗號、右括號等
    - 支援 // 開頭協定相對 URL 與 www. 開頭 URL
    - 僅保留 http/https 協定
    - 正規化網域大小寫與移除預設連接埠
    """
    from urllib.parse import urlparse, urlunparse

    if not url:
        return None

    url = url.strip().strip('\'"(),.;:!?]}>')

    # 直接忽略不需要的協定
    if url.startswith(("javascript:", "mailto:", "tel:", "#")):
        return None

    # 處理協定相對 URL
    if url.startswith("//"):
        url = "http:" + url

    # 補上 http 協定
    if url.startswith("www."):
        url = "http://" + url

    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return None

        netloc = parsed.netloc.lower().rstrip('.')
        # 去除預設連接埠
        if netloc.endswith(":80") and parsed.scheme == "http":
            netloc = netloc[:-3]
        if netloc.endswith(":443") and parsed.scheme == "https":
            netloc = netloc[:-4]

        path = parsed.path or "/"
        normalized = urlunparse((parsed.scheme, netloc, path, "", parsed.query, ""))
        return normalized
    except Exception:
        return None


def extract_urls(text: str, max_count: int = 50) -> list[str]:
    """從 HTML 或純文字中萃取網址並正規化。
    返回不重複的 http/https URL，最多 max_count 筆。
    """
    import re
    from bs4 import BeautifulSoup

    urls: set[str] = set()

    lowered = text.lower()

    # 若看起來像 HTML，先從 <a href> 萃取
    if "<html" in lowered or "<a " in lowered or "href=" in lowered:
        try:
            soup = BeautifulSoup(text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = (a.get("href") or "").strip()
                norm = _normalize_url(href)
                if norm:
                    urls.add(norm)
        except Exception:
            # 解析 HTML 失敗時忽略，改走正則
            pass

    # 以正則從純文字抓取 URL（含 www. 形式）
    pattern = re.compile(r"(?i)\b((?:https?://|www\.)[^\s<>\"'\)]{3,})")
    for m in pattern.finditer(text):
        cand = m.group(1)
        norm = _normalize_url(cand)
        if norm:
            urls.add(norm)

    # 回傳固定順序以利測試：依字典序排序後截斷
    result = sorted(urls)[:max_count]
    return result


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
