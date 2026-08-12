import requests
from pathlib import Path

state = "NC"
year = 2025

url = "https://ffiec.cfpb.gov/v2/data-browser-api/view/csv"f"?states={state}&years={year}&actions_taken=1,2,3,4,5,6,7,8"

dest = Path(f'data/raw/year={year}/state={state}/lar.csv')

dest.parent.mkdir(parents=True, exist_ok=True)


response = requests.get(url, stream = True)
response.raise_for_status()

with open(dest, "wb") as f:
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        f.write(chunk)

print(f"saved to {dest}")