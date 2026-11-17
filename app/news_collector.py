import re, feedparser
from app.config import get

def collect_sources() -> list[dict]:
    items=[]
    feeds=[u.strip() for u in get("RSS_FEEDS").split(",") if u.strip()]
    for url in feeds[:12]:
        try:
            parsed=feedparser.parse(url)
            for entry in parsed.entries[:4]:
                title=re.sub(r"\s+"," ",entry.get("title","")).strip()
                link=entry.get("link","").strip()
                summary=re.sub(r"<[^>]+>"," ",entry.get("summary",""))
                summary=re.sub(r"\s+"," ",summary).strip()[:600]
                if title and link:
                    items.append({"title":title,"summary":summary,"url":link})
        except Exception:
            continue
    return items[:30]
