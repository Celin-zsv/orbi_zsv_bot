"""This is the OrbiBot."""
from app.orbi_bot import run_polling, run_webhooks
from core.config import settings


def start():
    """Start bot."""
    if settings.webhook_mode:
        run_webhooks()
    else:
        run_polling()


if __name__ == "__main__":
    start()
