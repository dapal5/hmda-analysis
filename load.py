import duckdb

con = duckdb.connect("hmda.db")

con.sql("""
CREATE OR REPLACE TABLE raw AS
SELECT * 
FROM read_csv(
'data/raw/year=*/state=*/lar.csv',
all_varchar = true,
hive_partitioning = true,
union_by_name = true)""")

print(con.sql("SELECT COUNT(*) FROM raw").fetchone())

con.sql("SELECT year, state, COUNT(*) FROM raw GROUP BY 1, 2").show()

con.sql("SELECT COUNT(*) FROM raw WHERE action_taken IS NULL").show()