# ================================================================================
# =                                 RIVEN_SNIPER                                 =
# ================================================================================

import datetime
import logging

from aggregator import aggregator
from monitor import monitor
from poller import poller

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/riven_sniper.log"),
        logging.StreamHandler(),
    ],
)


def should_aggregate():
    """Check if it's 4am."""
    now = datetime.datetime.now()
    return now.hour == 4 and now.minute == 0


def riven_sniper():
    logging.info("Starting riven_sniper pipeline...")

    poller()

    if should_aggregate():
        aggregator()

    monitor()

    logging.info("Pipleline complete")
