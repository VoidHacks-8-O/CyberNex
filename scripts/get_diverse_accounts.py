import urllib.request
import json

def get_5_diverse_accounts():
    # 1. Top Threat Distributor
    req_radar = urllib.request.Request("http://127.0.0.1:8000/api/radar/metrics")
    with urllib.request.urlopen(req_radar) as res:
        radar = json.loads(res.read().decode("utf-8"))
    
    threats = radar.get("top_threats", [])
    print("TOP THREATS FROM DUCKDB RADAR:")
    for t in threats[:5]:
        print(t)

if __name__ == "__main__":
    get_5_diverse_accounts()
