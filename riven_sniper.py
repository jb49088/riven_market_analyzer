# ================================================================================
# =                                 RIVEN_SNIPER                                 =
# ================================================================================

import datetime
import logging
from pathlib import Path

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
    """Check if aggregator hasn't run today yet."""
    marker_file = Path("logs/.last_aggregate")
    today = datetime.date.today().isoformat()

    # Check if we already aggregated today
    if marker_file.exists():
        last_run = marker_file.read_text().strip()
        if last_run == today:
            return False

    # Only aggregate during 4am hour
    now = datetime.datetime.now()
    if now.hour == 4:
        marker_file.write_text(today)
        return True

    return False


def riven_sniper():
    logging.info("Starting riven_sniper pipeline...")

    try:
        poller()
    except Exception as e:
        logging.error(f"Poller failed: {e}")
        return

    if should_aggregate():
        try:
            aggregator()
        except Exception as e:
            logging.error(f"Aggregator failed: {e}")

    try:
        monitor()
    except Exception as e:
        logging.error(f"Monitor failed: {e}")

    logging.info("Pipeline complete")


if __name__ == "__main__":
    try:
        riven_sniper()
    except KeyboardInterrupt:
        logging.info("Riven sniper interrupted")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
