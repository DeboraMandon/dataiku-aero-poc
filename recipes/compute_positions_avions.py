import requests
try:
    r = requests.get("https://api.frankfurter.dev/v1/latest", timeout=15)
    print("Accès internet OK :", r.status_code)
except Exception as e:
    print("Accès internet KO :", e)