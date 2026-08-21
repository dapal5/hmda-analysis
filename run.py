import subprocess
import sys
import time

from logging_config import get_logger

logger = get_logger("run")


def run_step(name, cmd, **kwargs):
    logger.info(f"{name} starting")
    start = time.time()
    subprocess.run(cmd, check=True, **kwargs)
    logger.info(f"{name} completed in {time.time() - start:.1f}s")


def main():
    logger.info("Pipeline started")
    run_step("extract", [sys.executable, "extract.py"])
    run_step("load", [sys.executable, "load.py"])
    run_step("dbt build", ["dbt", "build"], cwd="hmda")
    logger.info("Pipeline complete")


if __name__ == "__main__":
    main()
