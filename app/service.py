import hashlib, json, logging
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal, PublishedPost
from app.ai_engine import generate_package, generate_image
from app.news_collector import collect_sources
from app.publishers import publish_telegram, publish_x
log=logging.getLogger("digo-social")

def publish_once() -> dict:
    data=generate_package(collect_sources())
    digest=hashlib.sha256(" ".join(data["telegram_text"].lower().split()).encode()).hexdigest()
    with SessionLocal() as db:
        if db.scalar(select(PublishedPost).where(PublishedPost.content_hash==digest)):
            return {"status":"duplicate_blocked"}
    stamp=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    image_path=f"media/digo-{stamp}.jpg"
    generate_image(data["image_prompt"],image_path)
    tg_id=""; x_id=""; errors=[]
    try:
        tg_id=publish_telegram(data["telegram_text"],image_path)
    except Exception as exc:
        log.exception("Telegram publishing failed")
        errors.append("Telegram: "+str(exc))
    try:
        x_id=publish_x(data["x_text"],image_path)
    except Exception as exc:
        log.exception("X publishing failed")
        errors.append("X: "+str(exc))
    with SessionLocal() as db:
        db.add(PublishedPost(topic=data["topic"],telegram_text=data["telegram_text"],
             x_text=data["x_text"],source_urls=json.dumps(data["source_urls"]),
             image_path=image_path,telegram_message_id=tg_id,x_post_id=x_id,content_hash=digest))
        try: db.commit()
        except IntegrityError: db.rollback()
    return {"status":"partial" if errors else "published","telegram_message_id":tg_id,
            "x_post_id":x_id,"errors":errors}
