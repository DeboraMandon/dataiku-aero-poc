import dataiku
import pandas as pd
import requests

TOKEN_URL = (
    "https://auth.opensky-network.org/auth/realms/opensky-network"
    "/protocol/openid-connect/token"
)
STATES_URL = "https://opensky-network.org/api/states/all"

DEFAULT_BBOX = {"lamin": 41.0, "lomin": -5.5, "lamax": 51.5, "lomax": 9.8}

STATE_VECTOR_COLUMNS = [
    "icao24", "callsign", "origin_country", "time_position", "last_contact",
    "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
    "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk",
    "spi", "position_source", "category",
]

client = dataiku.api_client()
project = client.get_default_project()
variables = project.get_variables()
client_id = variables["local"]["opensky_client_id"]
client_secret = variables["local"]["opensky_client_secret"]

payload = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}
token_response = requests.post(TOKEN_URL, data=payload, headers=headers, timeout=30)
token_response.raise_for_status()
token = token_response.json()["access_token"]

response = requests.get(
    STATES_URL,
    headers={"Authorization": f"Bearer {token}"},
    params=DEFAULT_BBOX,
    timeout=30,
)
response.raise_for_status()

data = response.json()
states = data.get("states") or []
columns = STATE_VECTOR_COLUMNS[: len(states[0])] if states else STATE_VECTOR_COLUMNS
df = pd.DataFrame(states, columns=columns)
df["query_time"] = data.get("time")

output = dataiku.Dataset("positions_avions")
output.write_with_schema(df)
