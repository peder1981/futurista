import pandas as pd
import world_bank_data as wb
import pycountry

def get_country_info(name):
    try:
        country = pycountry.countries.lookup(name)
        return pd.Series([country.alpha_3, country.name])
    except:
        return pd.Series([None, name])

def carregar_dados():
    inflation = wb.get_series("FP.CPI.TOTL.ZG", date="1990:2023", id_or_value="id").reset_index()
    interest = wb.get_series("FR.INR.RINR", date="1990:2023", id_or_value="id").reset_index()
    merged = pd.merge(inflation, interest, on=["Country", "Year"], how="inner")
    merged.rename(columns={
        "Country": "country_raw",
        "Year": "year",
        "FP.CPI.TOTL.ZG": "inflation",
        "FR.INR.RINR": "interest"
    }, inplace=True)
    merged[["iso3", "country"]] = merged["country_raw"].apply(get_country_info)
    merged["ratio"] = merged["interest"] / merged["inflation"]
    return merged[(merged["ratio"].notna()) & (merged["iso3"].notna()) & (merged["inflation"] > 0)]

