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

RACE = "C(derived_race, Treatment('White'))"

stages = {
    "1. RAW (race only)": f"denied ~ {RACE}",
    "2. + income, loan amount": f"denied ~ {RACE} + np.log(income) + np.log(loan_amount)",
    "3. + loan-to-value ratio": f"denied ~ {RACE} + np.log(income) + np.log(loan_amount) + loan_to_value_ratio",
    "4. + debt-to-income ratio": f"denied ~ {RACE} + np.log(income) + np.log(loan_amount) + loan_to_value_ratio + C(debt_to_income_ratio, Treatment('<20%'))",
}


def odds(model):
    keep = model.params.filter(like="derived_race")
    ci = model.conf_int().loc[keep.index]
    return pd.DataFrame({
        "odds_ratio": np.exp(keep),
        "ci_low": np.exp(ci[0]),
        "ci_high": np.exp(ci[1]),
    }).round(3)


for label, formula in stages.items():
    model = smf.logit(formula, data=df).fit(disp=0)
    print(label)
    print(odds(model), "\n")

alt = df[df["loan_to_value_ratio"] <= 100]
print(f"SENSITIVITY: LTV <= 100 instead of 120 (n={len(alt):,})")
alt_model = smf.logit(stages["4. + debt-to-income ratio"], data=alt).fit(disp=0)
print(odds(alt_model))
