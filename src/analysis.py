"""
Netflix streaming revenue analysis.

Segments revenue growth by region (UCAN, EMEA, LATAM, APAC), projects a
member/ARM-driven revenue path, sizes the ad-supported tier opportunity, and
quantifies the revenue impact of a churn reduction. Run
`python data/generate_data.py` first.
"""
from __future__ import annotations
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "outputs"

# Ad-tier assumptions (editable scenario inputs).
AD_TIER_PENETRATION = {"UCAN": 0.20, "EMEA": 0.18, "LATAM": 0.12, "APAC": 0.10}
AD_ARM_USD = {"UCAN": 9.0, "EMEA": 6.0, "LATAM": 4.0, "APAC": 3.5}


def load() -> tuple[pd.DataFrame, pd.DataFrame]:
    return pd.read_csv("data/regions.csv"), pd.read_csv("data/projections.csv")


def revenue_mix(regions: pd.DataFrame) -> pd.DataFrame:
    df = regions.copy()
    total = df["annual_rev_b"].sum()
    df["rev_share_pct"] = (df["annual_rev_b"] / total * 100).round(1)
    return df.sort_values("annual_rev_b", ascending=False)


def cagr_by_region(proj: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for region, g in proj.groupby("region"):
        g = g.sort_values("year")
        start, end = g.iloc[0]["annual_rev_b"], g.iloc[-1]["annual_rev_b"]
        years = g.iloc[-1]["year"] - g.iloc[0]["year"]
        cagr = (end / start) ** (1 / years) - 1
        rows.append({"region": region, "rev_2024_b": start,
                     "rev_2028_b": round(end, 2),
                     "cagr_pct": round(cagr * 100, 1)})
    return pd.DataFrame(rows).sort_values("cagr_pct", ascending=False)


def ad_tier_opportunity(regions: pd.DataFrame) -> pd.DataFrame:
    """Incremental annual ad-tier revenue if X% of members sit on the ad plan."""
    df = regions.copy()
    df["ad_members_m"] = df.apply(
        lambda r: r["members_m"] * AD_TIER_PENETRATION[r["region"]], axis=1)
    df["ad_rev_b"] = df.apply(
        lambda r: r["ad_members_m"] * AD_ARM_USD[r["region"]] * 12 / 1000, axis=1)
    df["ad_members_m"] = df["ad_members_m"].round(1)
    df["ad_rev_b"] = df["ad_rev_b"].round(2)
    return df[["region", "members_m", "ad_members_m", "ad_rev_b"]]


def churn_impact(regions: pd.DataFrame, churn_reduction_pct: float = 1.5) -> float:
    """Annual revenue retained from a churn reduction (pp of member base)."""
    retained_members = regions["members_m"] * (churn_reduction_pct / 100)
    retained_rev_b = (retained_members * regions["arm_usd"] * 12 / 1000).sum()
    return round(retained_rev_b, 2)


def plot_mix(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(df["region"], df["annual_rev_b"])
    for i, v in enumerate(df["annual_rev_b"]):
        ax.text(i, v + 0.3, f"${v}B", ha="center", fontsize=9)
    ax.set_title("Netflix annual revenue by region (~FY2024)")
    ax.set_ylabel("Revenue ($B)")
    fig.tight_layout()
    path = os.path.join(OUT, "fig_revenue_by_region.png")
    fig.savefig(path, dpi=120); plt.close(fig)
    return path


def plot_projection(proj: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(7, 4))
    for region, g in proj.groupby("region"):
        ax.plot(g["year"], g["annual_rev_b"], marker="o", label=region)
    ax.set_title("Projected Netflix revenue by region (2024-2028)")
    ax.set_ylabel("Revenue ($B)"); ax.set_xlabel("Year"); ax.legend()
    fig.tight_layout()
    path = os.path.join(OUT, "fig_projection.png")
    fig.savefig(path, dpi=120); plt.close(fig)
    return path


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    regions, proj = load()

    mix = revenue_mix(regions)
    print("\n=== Revenue mix by region (~FY2024) ===")
    print(mix.to_string(index=False))

    cagr = cagr_by_region(proj)
    print("\n=== Projected growth 2024-2028 (CAGR) ===")
    print(cagr.to_string(index=False))

    ad = ad_tier_opportunity(regions)
    print("\n=== Ad-tier opportunity (annual) ===")
    print(ad.to_string(index=False))
    print(f"Total incremental ad-tier revenue: ${ad['ad_rev_b'].sum():.2f}B/yr")

    retained = churn_impact(regions, 1.5)
    print(f"\n=== Churn impact ===\nA 1.5pp churn reduction retains "
          f"~${retained}B in annual revenue.")

    f1, f2 = plot_mix(mix), plot_projection(proj)
    mix.to_csv(os.path.join(OUT, "revenue_mix.csv"), index=False)
    cagr.to_csv(os.path.join(OUT, "cagr_by_region.csv"), index=False)
    print(f"\nSaved {f1}, {f2}, and outputs/*.csv")

    top = cagr.iloc[0]["region"]
    print("\n=== Recommendation ===")
    print(f"- {top} is the fastest-growing region "
          f"({cagr.iloc[0]['cagr_pct']}% CAGR) and the primary forward growth lever.")
    print("- The ad-supported tier adds a second lever, most impactful in "
          "price-sensitive regions where it expands the addressable base.")
    print(f"- Prioritize ad-tier expansion + retention: combined, the ad tier "
          f"(${ad['ad_rev_b'].sum():.1f}B/yr) and a modest churn reduction "
          f"(${retained}B/yr) are material to total revenue.")


if __name__ == "__main__":
    main()
