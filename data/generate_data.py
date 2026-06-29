"""
Generate the Netflix revenue dataset used in the analysis.

Seeded from Netflix's publicly filed 10-K / 10-Q segment disclosures and
quarterly shareholder letters (2021-2024 range). Regional membership and ARM
(average revenue per membership) are approximate, reproducible figures — not
audited values. Edit ASSUMPTIONS to run scenarios.
"""
from __future__ import annotations
import pandas as pd

# Netflix reports four revenue regions:
# UCAN (US & Canada), EMEA, LATAM, APAC.
# Approx. paid memberships (millions) and monthly ARM ($) by region, ~FY2024.
REGIONS = {
    "UCAN":  {"members_m": 89.6, "arm_usd": 17.30},
    "EMEA":  {"members_m": 96.1, "arm_usd": 11.00},
    "LATAM": {"members_m": 49.2, "arm_usd": 8.60},
    "APAC":  {"members_m": 50.3, "arm_usd": 7.40},
}

# Approx. annual member-growth and ARM-growth assumptions by region.
MEMBER_GROWTH = {"UCAN": 0.03, "EMEA": 0.08, "LATAM": 0.07, "APAC": 0.15}
ARM_GROWTH    = {"UCAN": 0.04, "EMEA": 0.05, "LATAM": 0.03, "APAC": 0.06}

BASE_YEAR = 2024
PROJECTION_YEARS = 4  # 2024 -> 2028


def regional_table() -> pd.DataFrame:
    rows = []
    for region, r in REGIONS.items():
        annual_rev_b = r["members_m"] * r["arm_usd"] * 12 / 1000  # $B/yr
        rows.append({
            "region": region,
            "members_m": r["members_m"],
            "arm_usd": r["arm_usd"],
            "annual_rev_b": round(annual_rev_b, 2),
        })
    return pd.DataFrame(rows)


def projection_table() -> pd.DataFrame:
    rows = []
    for region, r in REGIONS.items():
        members = r["members_m"]
        arm = r["arm_usd"]
        for i in range(PROJECTION_YEARS + 1):
            year = BASE_YEAR + i
            rev_b = members * arm * 12 / 1000
            rows.append({"region": region, "year": year,
                         "members_m": round(members, 1),
                         "arm_usd": round(arm, 2),
                         "annual_rev_b": round(rev_b, 2)})
            members *= (1 + MEMBER_GROWTH[region])
            arm *= (1 + ARM_GROWTH[region])
    return pd.DataFrame(rows)


def main() -> None:
    regional_table().to_csv("data/regions.csv", index=False)
    projection_table().to_csv("data/projections.csv", index=False)
    print("Wrote data/regions.csv and data/projections.csv")


if __name__ == "__main__":
    main()
