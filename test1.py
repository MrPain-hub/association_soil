import pandas as pd
from icecream import ic
import re

df = pd.read_excel(r"association_soil\data\stats_soil_1.xlsx")

out = []

for i in set(df["borehole"]):
    if re.search("Т", i):
        continue
    out.append(i)

df_out = pd.DataFrame({"borehole": out})
df_out.to_excel("test_out.xlsx")
