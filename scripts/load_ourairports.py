"""
Charge le référentiel aéroportuaire OurAirports dans la table `aeroports` (Neon).

Source des données : https://davidmegginson.github.io/ourairports-data/airports.csv
(domaine public, mis à jour quotidiennement par OurAirports.com)

Prérequis :
    pip install pandas sqlalchemy psycopg2-binary requests

Variables d'environnement attendues :
    NEON_CONNECTION_STRING   ex: postgresql://user:password@host/dbname?sslmode=require
    COUNTRY_FILTER           optionnel, code ISO pays à filtrer (défaut: FR)

Usage :
    python load_ourairports.py
"""

import os
import sys

import pandas as pd
import requests
from sqlalchemy import create_engine

OURAIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"

# Colonnes du CSV source -> colonnes de la table `aeroports`
COLUMN_MAP = {
    "id": "id",
    "ident": "ident",
    "type": "type",
    "name": "name",
    "latitude_deg": "latitude_deg",
    "longitude_deg": "longitude_deg",
    "elevation_ft": "elevation_ft",
    "continent": "continent",
    "iso_country": "iso_country",
    "iso_region": "iso_region",
    "municipality": "municipality",
    "icao_code": "icao_code",
    "iata_code": "iata_code",
    "gps_code": "gps_code",
    "local_code": "local_code",
}


def fetch_ourairports_csv() -> pd.DataFrame:
    response = requests.get(OURAIRPORTS_URL, timeout=60)
    response.raise_for_status()
    with open("_airports_raw.csv", "wb") as f:
        f.write(response.content)
    return pd.read_csv("_airports_raw.csv", low_memory=False)


def main() -> None:
    conn_string = os.environ.get("NEON_CONNECTION_STRING")
    if not conn_string:
        print("Erreur : la variable d'environnement NEON_CONNECTION_STRING est requise.")
        sys.exit(1)

    country_filter = os.environ.get("COUNTRY_FILTER", "FR")

    print(f"Téléchargement de {OURAIRPORTS_URL} ...")
    df = fetch_ourairports_csv()

    missing_cols = [c for c in COLUMN_MAP if c not in df.columns]
    if missing_cols:
        print(f"Attention : colonnes absentes du CSV source : {missing_cols}")

    available_cols = [c for c in COLUMN_MAP if c in df.columns]
    df = df[available_cols].rename(columns=COLUMN_MAP)

    if country_filter:
        before = len(df)
        df = df[df["iso_country"] == country_filter]
        print(f"Filtré sur iso_country={country_filter} : {before} -> {len(df)} lignes")

    engine = create_engine(conn_string)
    with engine.begin() as conn:
        conn.exec_driver_sql("TRUNCATE TABLE aeroports")
    df.to_sql("aeroports", engine, if_exists="append", index=False)
    print(f"{len(df)} lignes chargées dans la table `aeroports` sur Neon.")


if __name__ == "__main__":
    main()