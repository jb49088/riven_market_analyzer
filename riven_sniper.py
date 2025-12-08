# ================================================================================
# =                                 RIVEN_SNIPER                                 =
# ================================================================================

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


def riven_sniper():
    logging.info("Starting riven_sniper pipeline...")

    poller()
    aggregator()
    monitor()

    logging.info("Pipleline complete")
