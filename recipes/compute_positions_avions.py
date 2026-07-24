import dataiku
import pandas as pd
import requests

results = {}

for name, url in [
    ("frankfurter (test générique)", "https://api.frankfurter.dev/v1/latest"),
    ("opensky_auth", "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"),
]:
    try:
        r = requests.get(url, timeout=15)
        results[name] = f"OK - status {r.status_code}"
    except Exception as e:
        results[name] = f"ECHEC - {type(e).__name__}: {e}"

for name, result in results.items():
    print(f"{name} : {result}")

df = pd.DataFrame([{"test": k, "resultat": v} for k, v in results.items()])
output = dataiku.Dataset("positions_avions")
output.write_with_schema(df)