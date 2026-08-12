import requests

url = "https://ffiec.cfpb.gov/v2/data-browser-api/view/csv?states=NC&years=2025&actions_taken=1,2,3,4,5,6,7,8"

dest = 'data/raw/year=2025/state=NC/lar.csv'

response = requests.get(url, stream = True)
response.raise_for_status()

with open(dest, "wb") as f:
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        f.write(chunk)

print(f"saved to {dest}")