import logfire
from celery import Celery
from dotenv import load_dotenv

from stadt_bonn_oparl.config import BROKER_URL
from stadt_bonn_oparl.logging import configure_logging

load_dotenv()


configure_logging(2)
logfire.instrument_celery()

app = Celery(
    "stadt_bonn_oparl",
    broker=BROKER_URL,
    include=["stadt_bonn_oparl.tasks.files", "stadt_bonn_oparl.tasks.consultations"],
)

app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    app.start()
