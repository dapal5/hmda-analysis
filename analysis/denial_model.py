import duckdb
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

pd.set_option("display.width", None)
pd.set_option("display.max_columns", None) 

con = duckdb.connect("hmda.db", read_only=True)

df = con.sql("""
    SELECT
        denied,
        derived_race, derived_sex, age,
        income, loan_amount, loan_to_value_ratio,
        debt_to_income_ratio, loan_purpose, lien_status
    FROM int_universe
    WHERE derived_race IN ('White', 'Black or African American', 'Asian')
""").df()
con.close()

before = len(df)
df = df.dropna()
print(f"dropped {before - len(df)} incomplete rows")

before = len(df)
df = df[df["loan_to_value_ratio"] <= 120]
print(f"dropped {before - len(df)} LTV outliers")

before = len(df)
df = df[(df["income"] > 0) & (df["loan_amount"] > 0)]
print(f"dropped {before - len(df)} non-positive income/loan")
print(f"final sample: {len(df)}\n")

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