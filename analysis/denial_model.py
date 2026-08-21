import duckdb
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

pd.set_option("display.width", None)
pd.set_option("display.max_columns", None) 

con = duckdb.connect("hmda.db", read_only=True)

universe_n = con.sql("SELECT COUNT(*) FROM int_universe").fetchone()[0]
df = con.sql("SELECT * FROM int_regression_sample").df()
con.close()

print(f"int_universe: {universe_n:,} applications")
print(f"regression sample (3 races, complete cases, LTV <= 120): {len(df):,}\n")

m1 = smf.logit("denied ~ C(derived_race, Treatment('White'))", data=df).fit(disp=0)

m2 = smf.logit(
    "denied ~ C(derived_race, Treatment('White')) + np.log(income) + np.log(loan_amount) "
    "+ loan_to_value_ratio + C(debt_to_income_ratio, Treatment('<20%'))",
    data=df).fit(disp=0)

def odds(model):
    keep = model.params.filter(like="derived_race")
    ci = model.conf_int().loc[keep.index]
    return pd.DataFrame({
        "odds_ratio": np.exp(keep),
        "ci_low": np.exp(ci[0]),
        "ci_high": np.exp(ci[1]),
    }).round(3)

print("RAW (race only):")
print(odds(m1), "\n")
print("ADJUSTED (+ income, loan, LTV, DTI):")
print(odds(m2))