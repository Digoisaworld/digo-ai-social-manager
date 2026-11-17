import json, re, requests
from app.config import get, required
BASE = "https://gen.pollinations.ai"

def generate_package(sources: list[dict]) -> dict:
    required("POLLINATIONS_API_KEY")
    prompt = f"""You are the official English-language social editor for DIGO AI WORLD.
DIGO is an AI + Web3 community project on Solana. Brand identity: black, neon-lime green,
white and restrained gold; friendly futuristic dog mascot. Website:
https://digoisaworld.github.io/digo-website/
DIGO mint: 7gqusyDEx6L7JNUfDEUftzdKRSejgzCUk7QCUwocYG1F

Create one valuable content package for Telegram and X. Rotate topics across practical AI,
Web3 education, Solana ecosystem, blockchain safety, gaming, community engagement and
verified DIGO updates. Do not make every post an advertisement. Never invent partnerships,
listings, product features, milestones, token prices, rewards or airdrops. Never promise profit.
No financial advice or price predictions. If the source list is empty, write evergreen
educational content, not breaking news. Use only facts in supplied sources and cite URLs.
Telegram text: clear and engaging, maximum 850 characters.
X text: maximum 260 characters.
Image prompt: create a premium 16:9 DIGO visual, black/neon-lime/white/gold palette,
no tiny text, no fabricated logo lettering; a friendly futuristic dog mascot may appear.
Return only valid JSON with keys topic, telegram_text, x_text, image_prompt, source_urls.
Sources: {json.dumps(sources, ensure_ascii=False)}
"""
    response = requests.post(
        f"{BASE}/v1/chat/completions",
        headers={"Authorization": f"Bearer {get('POLLINATIONS_API_KEY')}", "Content-Type": "application/json"},
        json={"model": get("POLLINATIONS_TEXT_MODEL", "openai/gpt-5.4-nano"),
              "messages":[{"role":"user","content":prompt}], "temperature":0.7},
        timeout=120,
    )
    response.raise_for_status()
    payload = response.json()
    text = payload["choices"][0]["message"]["content"].strip()
    text = re.sub(r"^\x60{3}(?:json)?|\x60{3}$", "", text, flags=re.I).strip()
    data = json.loads(text)
    for field in ("topic","telegram_text","x_text","image_prompt"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"AI response missing {field}")
    data["x_text"] = data["x_text"][:277].rstrip() + ("…" if len(data["x_text"]) > 280 else "")
    data["source_urls"] = data.get("source_urls", [])
    return data

def generate_image(prompt: str, output_path: str) -> str:
    required("POLLINATIONS_API_KEY")
    import urllib.parse
    from pathlib import Path
    url = f"{BASE}/image/{urllib.parse.quote(prompt, safe='')}"
    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {get('POLLINATIONS_API_KEY')}"},
        params={"model":get("POLLINATIONS_IMAGE_MODEL","black-forest-labs/flux.1-schnell"),
                "width":1536,"height":1024,"nologo":"true"},
        timeout=240,
    )
    response.raise_for_status()
    if not response.headers.get("content-type","").startswith("image/"):
        raise RuntimeError("Pollinations did not return an image response")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_bytes(response.content)
    return output_path
