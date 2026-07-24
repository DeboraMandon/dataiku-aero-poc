"""
Récupère les statuts de vol pour chaque aéroport suivi (aeroports_suivis)
via l'API Aviationstack, en utilisant le référentiel Neon (aeroports) pour
convertir les codes ICAO en codes IATA attendus par l'API.

Remplace fetch_opensky.py : OpenSky bloque le trafic AWS (politique anti-abus
officielle, cf. docs/limites.md), donc injoignable depuis Dataiku Cloud.

Prérequis :
    pip install requests pandas sqlalchemy psycopg2-binary

Variables d'environnement attendues :
    AVIATIONSTACK_API_KEY
    NEON_CONNECTION_STRING

Usage en local :
    python fetch_aviationstack.py

Usage dans un recipe Python Dataiku :
    Remplacer la lecture CSV/Postgres locale par dataiku.Dataset(...).get_dataframe(),
    et la clé API par une variable projet locale plutôt qu'une variable d'environnement.
"""

import os
import sys
import time

import pandas as pd
import requests
from sqlalchemy import create_engine

BASE_URL = "https://api.aviationstack.com/v1/flights"


def load_aeroports_suivis(path: str = "../docs/aeroports_suivis_export.csv") -> pd.DataFrame:
    """En local, on n'a pas d'accès direct à Google Sheets sans credentials
    supplémentaires : ce script attend un export CSV de la feuille avec les
    colonnes code_icao, nom, priorite, commentaire."""
    return pd.read_csv(path)


def load_aeroports_ref(conn_string: str) -> pd.DataFrame:
    engine = create_engine(conn_string)
    return pd.read_sql("SELECT icao_code, iata_code FROM aeroports", engine)


def fetch_flights_for_airport(api_key: str, iata_code: str) -> list:
    params = {"access_key": api_key, "dep_iata": iata_code, "limit": 20}
    response = requests.get(BASE_URL, params=params, timeout=30)
    print(f"{iata_code} : status={response.status_code}")
    if response.status_code != 200:
        print(f"  -> réponse brute : {response.text[:300]}")
        return []
    data = response.json()
    if "error" in data:
        print(f"  -> erreur API : {data['error']}")
        return []
    flights = data.get("data") or []
    print(f"  -> {len(flights)} vols reçus")
    return flights


def main() -> None:
    api_key = os.environ.get("AVIATIONSTACK_API_KEY")
    conn_string = os.environ.get("NEON_CONNECTION_STRING")
    if not api_key or not conn_string:
        print("Erreur : AVIATIONSTACK_API_KEY et NEON_CONNECTION_STRING sont requis.")
        sys.exit(1)

    df_suivis = load_aeroports_suivis()
    df_ref = load_aeroports_ref(conn_string)

    df_join = df_suivis.merge(
        df_ref, left_on="code_icao", right_on="icao_code", how="left"
    )

    all_flights = []
    for _, row in df_join.iterrows():
        iata_code = row.get("iata_code")
        if pd.isna(iata_code) or not iata_code:
            print(f"Pas de code IATA pour {row['code_icao']}, on saute")
            continue
        flights = fetch_flights_for_airport(api_key, iata_code)
        for f in flights:
            f["aeroport_suivi_icao"] = row["code_icao"]
            f["aeroport_suivi_iata"] = iata_code
        all_flights.extend(flights)
        time.sleep(2)

    df = pd.json_normalize(all_flights) if all_flights else pd.DataFrame()
    df.to_csv("positions_avions.csv", index=False)
    print(f"Écrit dans positions_avions.csv ({len(df)} lignes)")


if __name__ == "__main__":
    main()