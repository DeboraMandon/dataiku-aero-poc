import dataiku
import pandas as pd
import requests

client = dataiku.api_client()
project = client.get_default_project()
variables = project.get_variables()
api_key = variables["local"]["aviationstack_api_key"]

aeroports_suivis = dataiku.Dataset("aeroports_suivis")
df_suivis = aeroports_suivis.get_dataframe()

all_flights = []
BASE_URL = "https://api.aviationstack.com/v1/flights"

for code_icao in df_suivis["code_icao"].dropna().unique():
    # Aviationstack utilise les codes IATA (3 lettres), pas ICAO (4 lettres)
    # On garde ICAO ici à titre indicatif ; un mapping ICAO->IATA sera
    # nécessaire (voir note ci-dessous)
    params = {
        "access_key": api_key,
        "dep_iata": code_icao[1:],  # placeholder, à corriger - voir note
        "limit": 20,
    }
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    flights = data.get("data") or []
    for f in flights:
        f["aeroport_suivi"] = code_icao
    all_flights.extend(flights)

df = pd.json_normalize(all_flights) if all_flights else pd.DataFrame()

output = dataiku.Dataset("positions_avions")
output.write_with_schema(df)