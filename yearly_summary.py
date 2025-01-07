import os
from datetime import date
import pandas as pd


data_dict = {}
all_years = []
for filename in os.listdir("data"):
    if not (filename.startswith("steps") and filename.endswith(".csv")):
        continue
    year = filename[5:9]
    print(f"found {year}")
    date_string = f"{year}-12-31"
    this_date = date.fromisoformat(date_string)
    if not this_date in all_years:
        all_years.append(this_date)
    df = pd.read_csv(os.path.join("data", filename))
    names = [c for c in df.columns if c != "Date"]
    for name in names:
        if not name in data_dict:
            data_dict[name] = {}
        data_dict[name][this_date] = int(df[name].sum())

all_names = list(data_dict.keys())

records = []
for year in sorted(all_years):
    year_dict = {"Date": year}
    for name in all_names:
        year_dict[name] = data_dict[name][year] if year in data_dict[name] else None
    records.append(year_dict)

df = pd.DataFrame(records)
