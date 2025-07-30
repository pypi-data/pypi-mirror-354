
import pandas as pd
df = pd.read_csv('/Users/danil/Downloads/Technographic Data .csv')

from verstack import DateParser

dp = DateParser()
dp.fit_transform(df)



date_pattern = (
    r"^(?!\d+\.\d+$)\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4}"  # Date part
    r"(?:[ T]\d{1,2}:\d{1,2}(?::\d{1,2})?)?"          # Optional time part with T or space
    r"(?:Z|(?:[ ]?(?:[A-Z]{1,5}(?:[+-]\d{1,2})?|[+-]\d{2}(?::?\d{2})?)))?$"  # All timezone formats
)
non_null_series = df['First Seen At'].dropna()

non_null_series.astype(str).str.contains(date_pattern, regex=True)