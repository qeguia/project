import pandas as pd
import requests
from io import StringIO

URL = "https://en.wikipedia.org/wiki/Ranked_lists_of_Spanish_autonomous_communities"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(URL, headers=headers)
tables = pd.read_html(StringIO(response.text))

df_pop = tables[0].copy()
df_pop.columns = ["comunidad", "poblacion_2024", "area_km2", "densidad_hab_km2", "costa_km"]
df_pop = df_pop[df_pop["comunidad"] != "Spain"]


df_income = tables[2][["Autonomous community", "Average income (€) 2023[2]"]].copy()
df_income.columns = ["comunidad", "renta_media_2023"]


df_gdp = tables[3][["Autonomous community", "GDP in billions €[3]", "Percentage of GDP"]].copy()
df_gdp.columns = ["comunidad", "pib_billones_eur", "pib_pct_nacional"]
df_gdp = df_gdp[df_gdp["comunidad"] != "Spain"]


df_gdppc = tables[4][["Autonomous community", "GDP per capita in €[4]"]].copy()
df_gdppc.columns = ["comunidad", "pib_per_capita"]
df_gdppc = df_gdppc[~df_gdppc["comunidad"].isin(["Spain", "European Union"])]
df_gdppc["pib_per_capita"] = df_gdppc["pib_per_capita"].astype(str).str.replace(",", "").str.extract(r"(\d+)").astype(float)


df_hdi = tables[5].copy()
df_hdi.columns = ["comunidad", "hdi_2022", "drop1", "drop2"]
df_hdi = df_hdi[["comunidad", "hdi_2022"]]
df_hdi = df_hdi[~df_hdi["comunidad"].isin(["Spain (average)"])]


name_map = {
    "Community of Madrid":  "Madrid",
    "Basque Country":       "País Vasco",
    "Balearic Islands":     "Baleares",
    "Canary Islands":       "Canarias",
    "Castile and León":     "Castilla y León",
    "Castilla–La Mancha":   "Castilla-La Mancha",
    "Valencian Community":  "C. Valenciana",
    "Catalonia":            "Cataluña",
    "Galicia":              "Galicia",
    "Andalusia":            "Andalucía",
    "Aragon":               "Aragón",
    "Asturias":             "Asturias",
    "Cantabria":            "Cantabria",
    "Extremadura":          "Extremadura",
    "Murcia":               "Murcia",
    "Navarre":              "Navarra",
    "La Rioja":             "La Rioja",
}

for df in [df_pop, df_income, df_gdp, df_gdppc, df_hdi]:
    df["comunidad"] = df["comunidad"].replace(name_map)


df = df_pop \
    .merge(df_income, on="comunidad", how="left") \
    .merge(df_gdp,    on="comunidad", how="left") \
    .merge(df_gdppc,  on="comunidad", how="left") \
    .merge(df_hdi,    on="comunidad", how="left")


df["pib_pct_nacional"] = df["pib_pct_nacional"].str.replace("%", "").astype(float)
df["hdi_2022"]         = pd.to_numeric(df["hdi_2022"], errors="coerce")


df["pib_per_habitante_check"] = (df["pib_billones_eur"] * 1e9 / df["poblacion_2024"]).round(0)
df["densidad_costera"]        = (df["costa_km"] / df["area_km2"]).round(4)  # coastal exposure

df = df.dropna(subset=["renta_media_2023"]).reset_index(drop=True)


print(df.head(5))
print(df.index)
print(df.columns)

