import requests, tweepy
from app.config import get, required

def _telegram_photo(chat_id: str, text: str, image_path: str) -> str:
    url=f"https://api.telegram.org/bot{get('TELEGRAM_BOT_TOKEN')}/sendPhoto"
    with open(image_path,"rb") as photo:
        r=requests.post(url,data={"chat_id":chat_id,"caption":text[:1024]},
                        files={"photo":photo},timeout=90)
    r.raise_for_status()
    body=r.json()
    if not body.get("ok"):
        raise RuntimeError(f"Telegram API returned: {body}")
    return str(body["result"]["message_id"])

def publish_telegram(text: str, image_path: str) -> dict:
    required("TELEGRAM_BOT_TOKEN","TELEGRAM_CHANNEL_ID")
    channel_message_id=_telegram_photo(get("TELEGRAM_CHANNEL_ID"),text,image_path)
    group_message_id=""
    if get("TELEGRAM_GROUP_ID"):
        group_message_id=_telegram_photo(get("TELEGRAM_GROUP_ID"),text,image_path)
    return {"channel_message_id":channel_message_id,"group_message_id":group_message_id}

def publish_x(text: str, image_path: str) -> str:
    required("X_API_KEY","X_API_SECRET","X_ACCESS_TOKEN","X_ACCESS_TOKEN_SECRET")
    auth=tweepy.OAuth1UserHandler(get("X_API_KEY"),get("X_API_SECRET"),
                                  get("X_ACCESS_TOKEN"),get("X_ACCESS_TOKEN_SECRET"))
    media=tweepy.API(auth).media_upload(filename=image_path)
    client=tweepy.Client(consumer_key=get("X_API_KEY"),consumer_secret=get("X_API_SECRET"),
                         access_token=get("X_ACCESS_TOKEN"),access_token_secret=get("X_ACCESS_TOKEN_SECRET"))
    result=client.create_tweet(text=text,media_ids=[media.media_id])
    return str(result.data["id"])
