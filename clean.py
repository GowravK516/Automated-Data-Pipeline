import requests
import pandas as pd

print("Fetching live data from API...")
response = requests.get("https://jsonplaceholder.typicode.com/users")

print("Processing with Pandas...")
df = pd.DataFrame(response.json())

df_cleaned = df[['id', 'name', 'username', 'email']]
df_cleaned.to_csv("live_dataset.csv", index=False)

print("Pipeline finished successfully!")
