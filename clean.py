import requests
import pandas as pd

print("Fetching live data from API...")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
response = requests.get("https://fakestoreapi.com/products", headers=headers)

print("Processing with Pandas...")
df = pd.DataFrame(response.json())

df_cleaned = df[['id', 'title', 'price', 'category']]
df_cleaned.to_csv("live_dataset.csv", index=False)

print("Pipeline finished successfully!")
