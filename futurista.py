import pandas as pd
import world_bank_data as wb
import pycountry
import plotly.express as px

print("🔧 Processando dados...")

# 1. Coleta de dados
inflation = wb.get_series("FP.CPI.TOTL.ZG", date="1990:2023", id_or_value="id")
interest = wb.get_series("FR.INR.RINR", date="1990:2023", id_or_value="id")

df_inflation = inflation.reset_index()
df_interest = interest.reset_index()

# 2. Merge dos dados
merged = pd.merge(df_inflation, df_interest, on=["Country", "Year"], how="inner")
merged.rename(columns={
    "Country": "country_raw",
    "Year": "year",
    "FP.CPI.TOTL.ZG": "inflation",
    "FR.INR.RINR": "interest"
}, inplace=True)

# 3. Adicionar código ISO3 e nome oficial do país
def get_country_info(name):
    try:
        country = pycountry.countries.lookup(name)
        return pd.Series([country.alpha_3, country.name])
    except:
        return pd.Series([None, name])  # fallback para nome original

merged[["iso3", "country"]] = merged["country_raw"].apply(get_country_info)

# 4. Calcular razão
merged["ratio"] = merged["interest"] / merged["inflation"]

# 5. Filtrar dados mais recentes e válidos
latest_year = merged["year"].max()
filtered = merged[
    (merged["year"] == latest_year) &
    (merged["ratio"].notna()) &
    (merged["iso3"].notna()) &
    (merged["inflation"] > 0)
]

# 6. Top 10 países
top_countries = filtered.sort_values("ratio", ascending=False).head(10)

# 7. Mapa interativo
fig = px.choropleth(
    filtered,
    locations="iso3",
    color="ratio",
    hover_name="country",
    color_continuous_scale="Viridis",
    title=f"🌐 Relação Juros Reais / Inflação — {latest_year}",
    labels={"ratio": "Juros / Inflação"}
)
fig.update_geos(showframe=False, showcoastlines=False)
fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
fig.write_html("mapa_juros_inflacao.html")
print("🗺️ Mapa salvo como: mapa_juros_inflacao.html")

# 8. Exportar CSV
top_countries[["country", "iso3", "year", "interest", "inflation", "ratio"]].to_csv("top_juros_inflacao.csv", index=False)
print("📁 CSV exportado como: top_juros_inflacao.csv")

# 9. Relatório Markdown
with open("relatorio_juros_inflacao.md", "w", encoding="utf-8") as f:
    f.write(f"# Relatório Econômico — {latest_year}\n\n")
    f.write("## 🏆 Top 10 países com maior relação entre juros reais e inflação\n\n")
    f.write("| País (nome oficial) | Código ISO3 | Ano | Juros (%) | Inflação (%) | Razão |\n")
    f.write("|---------------------|--------------|-----|------------|----------------|--------|\n")
    for _, row in top_countries.iterrows():
        f.write(f"| {row['country']} | {row['iso3']} | {int(row['year'])} | {row['interest']:.2f} | {row['inflation']:.2f} | {row['ratio']:.2f} |\n")
print("📝 Relatório gerado: relatorio_juros_inflacao.md")

