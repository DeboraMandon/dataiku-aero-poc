import time

BASE_URL = "https://api.aviationstack.com/v1/flights"
all_flights = []

for _, row in df_join.iterrows():
    iata_code = row.get("iata_code")
    if pd.isna(iata_code) or not iata_code:
        print(f"Pas de code IATA pour {row['code_icao']}, on saute")
        continue

    params = {
        "access_key": api_key,
        "dep_iata": iata_code,
        "limit": 20,
    }
    response = requests.get(BASE_URL, params=params, timeout=30)
    print(f"{row['code_icao']} ({iata_code}) : status={response.status_code}")

    if response.status_code != 200:
        print(f"  -> réponse brute : {response.text[:300]}")
        continue

    data = response.json()
    if "error" in data:
        print(f"  -> erreur API : {data['error']}")
        continue

    flights = data.get("data") or []
    print(f"  -> {len(flights)} vols reçus")
    for f in flights:
        f["aeroport_suivi_icao"] = row["code_icao"]
        f["aeroport_suivi_iata"] = iata_code
    all_flights.extend(flights)

    time.sleep(2)  # pause pour éviter le rate limit

df = pd.json_normalize(all_flights) if all_flights else pd.DataFrame()

output = dataiku.Dataset("positions_avions")
output.write_with_schema(df)