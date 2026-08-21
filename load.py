import duckdb

from logging_config import get_logger

logger = get_logger("load")


def main():
    logger.info("Load started")
    con = duckdb.connect("hmda.db")

    con.sql("""
    CREATE OR REPLACE TABLE raw AS
    SELECT *
    FROM read_csv(
        'data/raw/year=*/state=*/lar.csv',
        all_varchar = true,
        hive_partitioning = true,
        union_by_name = true)
    """)

    total = con.sql("SELECT COUNT(*) FROM raw").fetchone()[0]
    logger.info(f"Loaded {total:,} rows into raw table")

    for year, state, count in con.sql(
        "SELECT year, state, COUNT(*) FROM raw GROUP BY 1, 2"
    ).fetchall():
        logger.info(f"partition year={year} state={state}: {count:,} rows")

    null_actions = con.sql(
        "SELECT COUNT(*) FROM raw WHERE action_taken IS NULL"
    ).fetchone()[0]
    logger.info(f"{null_actions:,} rows have a null action_taken")

    con.close()
    logger.info("Load complete")


if __name__ == "__main__":
    main()
