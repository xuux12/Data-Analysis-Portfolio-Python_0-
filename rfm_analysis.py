import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings

warnings.filterwarnings("ignore")

# Load dataset
df = pd.read_excel("data/online_retail_data.xlsx", parse_dates=["InvoiceDate"])
df.dropna(subset=["CustomerID"], inplace=True)
df = df[df["Quantity"] > 0]
df["TotalSales"] = df["Quantity"] * df["UnitPrice"]

# RFM Calculation
snapshot_date = df["InvoiceDate"].max()
rfm = df.groupby("CustomerID").agg({
    "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
    "InvoiceNo": "count",
    "TotalSales": "sum"
})
rfm.columns = ["Recency", "Frequency", "Monetary"]

# Normalize
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)

# KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
rfm["Cluster"] = kmeans.fit_predict(rfm_scaled) + 1

# Save result
rfm.to_csv("rfm_clustered.csv")
