import requests
try:
    r = requests.get("https://opensky-network.org", timeout=15)
    print("opensky-network.org (racine) :", r.status_code)
except Exception as e:
    print("opensky-network.org (racine) : ECHEC -", type(e).__name__, str(e))