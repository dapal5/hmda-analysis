from pathlib import Path

import requests

from logging_config import get_logger

logger = get_logger("extract")

STATE = "NC"
YEAR = 2025


def main():
    url = (
        "https://ffiec.cfpb.gov/v2/data-browser-api/view/csv"
        f"?states={STATE}&years={YEAR}&actions_taken=1,2,3,4,5,6,7,8"
    )
    dest = Path(f"data/raw/year={YEAR}/state={STATE}/lar.csv")
    dest.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Extraction started for state={STATE} year={YEAR}")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    line_count = 0
    with open(dest, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
            line_count += chunk.count(b"\n")

    logger.info(f"Downloaded {line_count - 1:,} records to {dest}")


if __name__ == "__main__":
    main()
