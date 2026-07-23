"""
Récupère les positions d'avions en direct depuis l'API OpenSky Network,
sur une bounding box donnée, via authentification OAuth2 client credentials
(obligatoire depuis le retrait de l'authentification basique en mars 2026).

Prérequis :
    pip install requests pandas

Variables d'environnement attendues :
    OPENSKY_CLIENT_ID
    OPENSKY_CLIENT_SECRET

Usage en local :
    python fetch_opensky.py

Usage dans un recipe Python Dataiku :
    Copier get_token() et get_states() dans le recipe, stocker les credentials
    dans les "project variables" / credentials Dataiku plutôt qu'en dur, puis
    écrire le DataFrame résultat avec :
        import dataiku
        dataiku.Dataset("positions_avions").write_with_schema(df)
"""

import os
import sys
import time

import pandas as pd
import requests

TOKEN_URL = (
    "https://auth.opensky-network.org/auth/realms/opensky-network"
    "/protocol/openid-connect/token"
)
STATES_URL = "https://opensky-network.org/api/states/all"

# Bounding box par défaut : France métropolitaine (lamin, lomin, lamax, lomax)
DEFAULT_BBOX = {
    "lamin": 41.0,
    "lomin": -5.5,
    "lamax": 51.5,
    "lomax": 9.8,
}

STATE_VECTOR_COLUMNS = [
    "icao24", "callsign", "origin_country", "time_position", "last_contact",
    "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
    "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk",
    "spi", "position_source", "category",
]


def get_token(client_id: str, client_secret: str) -> str:
    """Échange client_id/client_secret contre un access token Bearer.
    Le token expire après ~30 minutes : à ré-appeler avant chaque run planifié
    plutôt qu'à mettre en cache longtemps."""
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(TOKEN_URL, data=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()["access_token"]


def get_states(token: str, bbox: dict = DEFAULT_BBOX) -> pd.DataFrame:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(STATES_URL, headers=headers, params=bbox, timeout=30)
    response.raise_for_status()

    remaining = response.headers.get("X-Rate-Limit-Remaining")
    if remaining is not None:
        print(f"Quota restant (X-Rate-Limit-Remaining) : {remaining}")

    data = response.json()
    states = data.get("states") or []

    if states:
        n_cols = len(states[0])
        columns = STATE_VECTOR_COLUMNS[:n_cols]
    else:
        columns = STATE_VECTOR_COLUMNS

    df = pd.DataFrame(states, columns=columns)
    df["query_time"] = data.get("time")
    return df


def main() -> None:
    client_id = os.environ.get("OPENSKY_CLIENT_ID")
    client_secret = os.environ.get("OPENSKY_CLIENT_SECRET")
    if not client_id or not client_secret:
        print("Erreur : OPENSKY_CLIENT_ID et OPENSKY_CLIENT_SECRET sont requis.")
        sys.exit(1)

    token = get_token(client_id, client_secret)
    df = get_states(token)

    print(f"{len(df)} avions détectés dans la bounding box à t={int(time.time())}")
    print(df[["icao24", "callsign", "origin_country", "baro_altitude", "velocity"]].head(10))

    df.to_csv("positions_avions.csv", index=False)
    print("Écrit dans positions_avions.csv")


if __name__ == "__main__":
    main()