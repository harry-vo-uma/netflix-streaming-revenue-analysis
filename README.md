# Streaming Market Revenue Analysis — Netflix

Analyzes Netflix's revenue drivers using public 10-K / quarterly filings,
segmenting growth by region (**UCAN, EMEA, LATAM, APAC**) to identify the
primary forward growth levers, size the **ad-supported tier** opportunity, and
quantify the revenue impact of a churn reduction.

## What it does
- Builds a reproducible dataset of regional paid memberships and ARM (average
  revenue per membership) from Netflix's public segment disclosures.
- Computes the **revenue mix** by region and a member/ARM-driven **projection**
  with per-region CAGR.
- Sizes the **ad-supported tier** opportunity under editable penetration / ad-ARM
  assumptions.
- Runs a **churn sensitivity** to quantify revenue retained from a 0.5–2.0pp
  churn reduction.

## Quickstart
```bash
pip install -r requirements.txt
python data/generate_data.py     # writes data/regions.csv, data/projections.csv
python src/analysis.py           # prints metrics, saves figures to outputs/
```
Or open `notebooks/netflix_streaming_revenue_analysis.ipynb`.

## Structure
```
data/generate_data.py   # assumptions + dataset generation (edit for scenarios)
src/analysis.py         # revenue mix, CAGR, ad-tier sizing, churn impact, figures
notebooks/              # narrative analysis notebook
outputs/                # generated figures + CSVs
```

## Data disclaimer
Regional memberships and ARM are approximated from Netflix's publicly filed
disclosures and shareholder letters. These are reproducible **estimates**, not
audited values. Edit the assumptions in `data/generate_data.py` and `src/analysis.py`.

## Author
Harry Vo — https://github.com/harry-vo-uma
