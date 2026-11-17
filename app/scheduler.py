import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from apscheduler.schedulers.blocking import BlockingScheduler
from app.config import get
from app.service import publish_once
logging.basicConfig(level=get("LOG_LEVEL","INFO"))
log=logging.getLogger("digo-scheduler")

def run_job():
    try: log.info("Publish result: %s",publish_once())
    except Exception: log.exception("Scheduled publishing failed")

def main():
    tz=ZoneInfo(get("TIMEZONE","Asia/Tehran"))
    days=max(1,int(get("POST_INTERVAL_DAYS","3")))
    hour=max(0,min(23,int(get("POST_HOUR","12"))))
    minute=max(0,min(59,int(get("POST_MINUTE","0"))))
    now=datetime.now(tz)
    first=now.replace(hour=hour,minute=minute,second=0,microsecond=0)
    if first<=now: first+=timedelta(days=1)
    scheduler=BlockingScheduler(timezone=tz)
    scheduler.add_job(run_job,"interval",days=days,next_run_time=first,
                      id="digo-posting",max_instances=1,coalesce=True)
    log.info("Scheduler enabled: every %s day(s), first run %s",days,first)
    scheduler.start()

if __name__=="__main__": main()
