"""
CLTV Prediction using BG/NBD and Gamma-Gamma Models
FLO Customer Lifetime Value Case Study
"""

import pandas as pd
import datetime as dt
from lifetimes import BetaGeoFitter, GammaGammaFitter

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.options.mode.chained_assignment = None


def outlier_thresholds(dataframe, variable):
    """Calculates lower and upper outlier thresholds using the IQR method."""
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit


def replace_with_thresholds(dataframe, variable):
    """Caps outlier values at the calculated thresholds (rounded, since CLTV requires integer-like frequency)."""
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = round(low_limit, 0)
    dataframe.loc[(dataframe[variable] > up_limit), variable] = round(up_limit, 0)


def create_cltv_df(dataframe):
    """
    Prepares the dataset and calculates 6-month CLTV predictions using
    BG/NBD (expected purchase frequency) and Gamma-Gamma (expected average
    profit) models.

    Returns a dataframe with CLTV scores and segments (A-D, A being highest value).
    """

    # --- Outlier suppression ---
    columns = ["order_num_total_ever_online", "order_num_total_ever_offline",
               "customer_value_total_ever_offline", "customer_value_total_ever_online"]
    for col in columns:
        replace_with_thresholds(dataframe, col)

    # --- Feature engineering (omnichannel totals) ---
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    dataframe = dataframe[~(dataframe["customer_value_total"] == 0) | (dataframe["order_num_total"] == 0)]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)

    # --- CLTV base structure (recency, tenure, frequency, monetary) ---
    analysis_date = dt.datetime(2021, 6, 1)
    cltv_df = pd.DataFrame()
    cltv_df["customer_id"] = dataframe["master_id"]
    cltv_df["recency_cltv_weekly"] = (dataframe["last_order_date"] - dataframe["first_order_date"]).dt.days / 7
    cltv_df["T_weekly"] = (analysis_date - dataframe["first_order_date"]).dt.days / 7
    cltv_df["frequency"] = dataframe["order_num_total"]
    cltv_df["monetary_cltv_avg"] = dataframe["customer_value_total"] / dataframe["order_num_total"]

    # BG/NBD requires repeat purchase behavior, so single-purchase customers are excluded
    cltv_df = cltv_df[(cltv_df['frequency'] > 1)]

    # --- BG/NBD model: expected purchase frequency ---
    bgf = BetaGeoFitter(penalizer_coef=0.001)
    bgf.fit(cltv_df['frequency'], cltv_df['recency_cltv_weekly'], cltv_df['T_weekly'])
    cltv_df["exp_sales_3_month"] = bgf.predict(4 * 3, cltv_df['frequency'], cltv_df['recency_cltv_weekly'], cltv_df['T_weekly'])
    cltv_df["exp_sales_6_month"] = bgf.predict(4 * 6, cltv_df['frequency'], cltv_df['recency_cltv_weekly'], cltv_df['T_weekly'])

    # --- Gamma-Gamma model: expected average profit per transaction ---
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(cltv_df['frequency'], cltv_df['monetary_cltv_avg'])
    cltv_df["exp_average_value"] = ggf.conditional_expected_average_profit(cltv_df['frequency'], cltv_df['monetary_cltv_avg'])

    # --- Final 6-month CLTV calculation & segmentation ---
    cltv = ggf.customer_lifetime_value(bgf, cltv_df['frequency'], cltv_df['recency_cltv_weekly'],
                                        cltv_df['T_weekly'], cltv_df['monetary_cltv_avg'],
                                        time=6, freq="W", discount_rate=0.01)
    cltv_df["cltv"] = cltv
    cltv_df["cltv_segment"] = pd.qcut(cltv_df["cltv"], 4, labels=["D", "C", "B", "A"])

    return cltv_df


df = pd.read_csv("datasets/flo_data_20k.csv")
cltv_df = create_cltv_df(df)
print(cltv_df.sort_values("cltv", ascending=False).head(20))
