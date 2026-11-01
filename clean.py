import requests
import pandas as pd

print("Fetching live data from API...")
response = requests.get("https://fakestoreapi.com/products")

print("Processing with Pandas...")
df = pd.DataFrame(response.json())

df_cleaned = df[['id', 'title', 'price', 'category']]
df_cleaned.to_csv("live_dataset.csv", index=False)

print("Pipeline finished successfully!")
