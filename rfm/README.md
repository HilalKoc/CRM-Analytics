# RFM Customer Segmentation - FLO Case Study

## Business Problem

FLO wants to segment its customers and define marketing strategies based on these segments. Customer purchasing behavior will be analyzed and customers will be grouped according to these behavioral clusters.

## Dataset

| File | Description |
|---|---|
| `flo_data_20K.csv` | Purchase history of OmniChannel customers (both online and offline) who shopped between 2020-2021 |

Key fields include order channel, first/last order dates (online & offline), total number of orders, total spending, and product categories purchased in the last 12 months.

## Methodology

| Step | Description |
|---|---|
| Step 1 | Data understanding & preparation (missing values, data types, omnichannel total order/spending variables) |
| Step 2 | Calculate RFM metrics (Recency, Frequency, Monetary) |
| Step 3 | Convert RFM metrics into 1–5 scores using `pd.qcut` |
| Step 4 | Map RF scores into named customer segments (e.g. champions, at_risk, hibernating) |
| Step 5 | Take action — identify target customer groups for two real marketing scenarios |
| Step 6 | Wrap the entire pipeline into a single reusable function (`create_rfm`) |

## Results — Segment Profiles

Average Recency (days since last purchase), Frequency (total orders), and Monetary (total spending) values per segment:

| Segment | Avg. Recency | Count | Avg. Frequency | Avg. Monetary |
|---|---|---|---|---|
| champions | 17.11 | 1,932 | 8.93 | 1,406.63 |
| loyal_customers | 82.59 | 3,361 | 8.37 | 1,216.82 |
| cant_loose | 235.44 | 1,200 | 10.70 | 1,474.47 |
| at_Risk | 241.61 | 3,131 | 4.47 | 646.61 |
| hibernating | 247.95 | 3,604 | 2.39 | 366.27 |
| about_to_sleep | 113.79 | 1,629 | 2.40 | 359.01 |
| need_attention | 113.83 | 823 | 3.73 | 562.14 |
| potential_loyalists | 37.16 | 2,938 | 3.30 | 533.18 |
| promising | 58.92 | 647 | 2.00 | 335.67 |
| new_customers | 17.92 | 680 | 2.00 | 339.96 |

**Key insight:** `cant_loose` customers have the highest average monetary value (1,474.47) despite not having purchased recently (235 days) — these are high-value customers at risk of churn, making them a priority for re-engagement.

## Business Actions

Two real marketing scenarios were addressed using the segmentation:

**a) New premium women's shoe brand launch**
Target audience: loyal customers (`champions`, `loyal_customers`) who have purchased from the `KADIN` (women's) category — since the new brand is priced above average, only proven high-value female-category shoppers were targeted.
→ Exported to `yeni_marka_hedef_müşteri_id.csv`

**b) 40% discount campaign on men's & children's products**
Target audience: previously valuable customers now at risk of churn or newly acquired (`cant_loose`, `hibernating`, `new_customers`) who have shown interest in `ERKEK` (men's) or `COCUK` (children's) categories — aiming to re-activate lapsed high-value customers and convert new ones.
→ Exported to `indirim_hedef_müşteri_ids.csv`

## Conclusion

RFM segmentation turns raw transaction history into actionable customer groups without requiring any predictive modeling. In this case, it enabled two clearly targeted, ROI-driven marketing actions — a premium product launch aimed at proven high spenders, and a win-back discount campaign aimed at high-value customers who are slipping away. The entire pipeline was wrapped into a single function (`create_rfm`), making it reusable for future campaigns on updated data.

## Topics Covered

- RFM (Recency, Frequency, Monetary) analysis
- Customer segmentation with `pd.qcut`
- Regex-based segment mapping
- Business-driven customer targeting
- Function-based, reusable data pipeline design

## Tools & Libraries

- Python 3.x
- pandas
- datetime

---
*This project was completed as part of the MIUUL Data Analyst Path program.*
