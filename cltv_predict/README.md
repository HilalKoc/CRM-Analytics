# CLTV Prediction with BG/NBD & Gamma-Gamma - FLO Case Study

## Business Problem

FLO wants to set a roadmap for its sales and marketing activities. To support mid-to-long-term planning, the company needs to estimate the potential future value that existing customers will bring — not just their past purchase behavior, but their expected value over the next 6 months.

## Dataset

| File | Description |
|---|---|
| `flo_data_20k.csv` | Purchase history of OmniChannel customers (both online and offline) who shopped between 2020-2021 |

## Methodology

| Step | Description |
|---|---|
| Step 1 | Suppress outliers in order count and spending variables (IQR method) |
| Step 2 | Build omnichannel total order/spending features |
| Step 3 | Construct the CLTV base structure: recency, tenure (T), frequency, and average monetary value per transaction (weekly units) |
| Step 4 | Fit the **BG/NBD model** to predict expected number of purchases in 3 and 6 months |
| Step 5 | Fit the **Gamma-Gamma model** to predict the expected average profit per transaction |
| Step 6 | Combine both models to calculate 6-month CLTV, then segment customers into 4 groups (A–D) based on predicted value |

**Note on data preparation:** The BG/NBD model estimates repeat purchase behavior, which cannot be meaningfully modeled from a single transaction. Customers with `frequency <= 1` were therefore excluded before model fitting.

## Results

**Dataset after filtering:** 19,945 customers with repeat purchases

**Overall CLTV distribution:**

| Statistic | Value |
|---|---|
| Mean | 195.12 |
| Median | 165.47 |
| Min | 12.11 |
| Max | 3,327.78 |

**Segment profiles (6-month CLTV):**

| Segment | Avg. CLTV | Count | Avg. Expected Purchases (6mo) | Avg. Transaction Value |
|---|---|---|---|---|
| A | 362.32 | 4,986 | 1.55 | 228.83 |
| B | 199.53 | 4,986 | 1.20 | 160.64 |
| C | 138.31 | 4,986 | 1.05 | 125.79 |
| D | 80.34 | 4,987 | 0.82 | 93.15 |

The highest-value customer in the dataset has a predicted 6-month CLTV of 3,327.78 — driven primarily by a high average transaction value (1,401.80) rather than high purchase frequency (4 orders), showing that both dimensions can independently push a customer into the top-value tier.

## Segmentation Interpretation

Dividing customers into 4 CLTV-based segments (A–D) produces a fairly consistent, proportional increase between segments B, C, and D:

- C/D ratio: 138.31 / 80.34 ≈ 1.72x
- B/C ratio: 199.53 / 138.31 ≈ 1.44x
- A/B ratio: 362.32 / 199.53 ≈ 1.82x

The jump from B to A is proportionally larger than the increases between the other segments, suggesting that Segment A covers a wider value range than the others. This is also visible when comparing Segment A's average CLTV (362.32) to the maximum value in the dataset (3,327.78) — nearly 9 times higher than the segment average.

Based on this, 4 segments remain a reasonable and practical starting point for reporting to management. However, splitting Segment A further (e.g. isolating the top-performing customers within it) could allow for more precise targeting, since customers at the very top of Segment A appear to generate substantially more value than the segment average suggests.

## Business Recommendations

**Segment A — Highest-value customers**
This segment combines high purchase frequency with high transaction value. Recommended 6-month action: a dedicated loyalty program with early access to new products and personalized offers, aimed at retention — losing customers from this segment would disproportionately impact future revenue.

**Segment D — Lower-value but still active customers**
Although this segment has the lowest predicted CLTV, these customers have already made at least one repeat purchase. Recommended 6-month action: cross-sell campaigns and low-cost incentives (e.g. small discount coupons) aimed at increasing both transaction value and purchase frequency.

## Conclusion

Unlike rule-based segmentation (e.g. RFM), this approach uses probabilistic models to *predict* future customer value rather than only describing past behavior. Combining BG/NBD (purchase frequency) and Gamma-Gamma (transaction value) models allowed FLO's customer base to be ranked by expected 6-month value, enabling more forward-looking marketing and retention decisions. The entire pipeline is wrapped into a single reusable function (`create_cltv_df`), making it straightforward to re-run on updated data.

## Topics Covered

- Outlier detection and suppression (IQR method)
- Probabilistic customer lifetime value modeling
- BG/NBD model (expected transaction frequency)
- Gamma-Gamma model (expected transaction value)
- CLTV-based customer segmentation

## Tools & Libraries

- Python 3.x
- pandas
- lifetimes (BetaGeoFitter, GammaGammaFitter)

---
*This project was completed as part of the MIUUL Data Analyst Path program.*
