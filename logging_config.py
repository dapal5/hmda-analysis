import logging
from pathlib import Path


def get_logger(name):
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("logs/pipeline.log"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(name)
