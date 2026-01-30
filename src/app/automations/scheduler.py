from apscheduler.schedulers.background import BackgroundScheduler

from app.database.session import SessionLocal
from app.modules.automations.service import update_overdue_obligations


def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        func=run_update_overdue,
        trigger="interval",
        hours=24,
        id="update_overdue_obligations",
        replace_existing=True,
    )

    scheduler.start()


def run_update_overdue():
    db = SessionLocal()
    try:
        update_overdue_obligations(db)
    finally:
        db.close()
