import requests
import pandas as pd
import numpy as np
from datetime import datetime, timezone

print("Step 1: Fetching live base records from external REST APIs...")
users_resp = requests.get("https://jsonplaceholder.typicode.com/users")
todos_resp = requests.get("https://jsonplaceholder.typicode.com/todos")

users_df = pd.DataFrame(users_resp.json())[['id', 'name', 'username', 'email']]
todos_df = pd.DataFrame(todos_resp.json())

# Merge user profiles with activity logs (200 base records)
merged_df = pd.merge(todos_df, users_df, left_on='userId', right_on='id', suffixes=('_task', '_user'))

print("Step 2: Scaling to 5,200 raw transaction records with real-world data anomalies...")
np.random.seed(42)
raw_df = pd.concat([merged_df] * 26, ignore_index=True)
raw_df['transaction_id'] = np.arange(100001, 100001 + len(raw_df))
raw_df['raw_amount_inr'] = np.random.uniform(150.0, 15000.0, size=len(raw_df)).round(2)

# Inject realistic messy data (Null values, negative errors, and duplicate rows)
raw_df.loc[raw_df.sample(frac=0.06).index, 'raw_amount_inr'] = np.nan
raw_df.loc[raw_df.sample(frac=0.03).index, 'email'] = None
raw_df.loc[raw_df.sample(frac=0.02).index, 'raw_amount_inr'] = -500.00
raw_df = pd.concat([raw_df, raw_df.iloc[:150]], ignore_index=True)

print(f"--> Raw Ingested Dataset Shape: {raw_df.shape[0]} rows, {raw_df.shape[1]} columns")
print(f"--> Detected Null Values:\n{raw_df[['raw_amount_inr', 'email']].isnull().sum()}\n")

print("Step 3: Executing Pandas ETL Data Cleaning & Feature Engineering...")
# 1. Remove exact duplicate transactions
df_clean = raw_df.drop_duplicates(subset=['transaction_id']).copy()

# 2. Drop rows where critical customer email is missing
df_clean = df_clean.dropna(subset=['email'])

# 3. Filter out corrupted negative transaction amounts
df_clean = df_clean[df_clean['raw_amount_inr'] > 0]

# 4. Impute missing transaction amounts using each user's median spend
df_clean['raw_amount_inr'] = df_clean['raw_amount_inr'].fillna(
    df_clean.groupby('userId')['raw_amount_inr'].transform('median')
)

# 5. Text standardization (lowercase emails, clean whitespace, extract domain)
df_clean['email'] = df_clean['email'].str.strip().str.lower()
df_clean['email_domain'] = df_clean['email'].apply(lambda x: x.split('@')[-1])
df_clean['name'] = df_clean['name'].str.strip().str.title()

# 6. Financial Feature Engineering: 18% GST calculation & High-Value Tiering
df_clean['gst_18_percent'] = (df_clean['raw_amount_inr'] * 0.18).round(2)
df_clean['final_billed_inr'] = (df_clean['raw_amount_inr'] + df_clean['gst_18_percent']).round(2)
df_clean['customer_tier'] = np.where(df_clean['final_billed_inr'] >= 10000, 'Enterprise', 
                            np.where(df_clean['final_billed_inr'] >= 5000, 'Premiere', 'Standard'))
df_clean['processed_at_utc'] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

# Select final structured analytical schema
final_cols = [
    'transaction_id', 'userId', 'name', 'username', 'email', 'email_domain',
    'raw_amount_inr', 'gst_18_percent', 'final_billed_inr', 'customer_tier',
    'completed', 'processed_at_utc'
]
df_clean = df_clean[final_cols]

# Save both the full 5,000+ row dataset and overwrite dataset.csv so both are huge
df_clean.to_csv("live_dataset.csv", index=False)
df_clean.to_csv("dataset.csv", index=False)

print(f"--> Cleaned Dataset Shape: {df_clean.shape[0]} rows, {df_clean.shape[1]} columns")
print("--> Transformation Summary (Removed duplicates, imputed NaNs, added GST & Tiers):")
print(df_clean[['transaction_id', 'name', 'email', 'final_billed_inr', 'customer_tier']].head(10).to_string(index=False))
print("\nPipeline finished successfully! Saved 5,000+ cleaned records to dataset.csv and live_dataset.csv.")
