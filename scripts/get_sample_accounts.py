import urllib.request
import json

def get_real_accounts():
    # 1. Fetch top threats from radar
    req = urllib.request.Request("http://127.0.0.1:8000/api/radar/metrics")
    with urllib.request.urlopen(req) as res:
        radar = json.loads(res.read().decode("utf-8"))

    top_threats = [t["account_id"] for t in radar.get("top_threats", [])]

    # 2. Let's find some pure senders and pure receivers by querying accounts
    test_prefixes = ["HDFC", "SBIN", "ICIC", "AIRP", "PUNB", "AXIS", "KKBK", "YESB"]
    found_accounts = []
    for prefix in test_prefixes:
        req_s = urllib.request.Request(f"http://127.0.0.1:8000/api/accounts/search?q={prefix}")
        with urllib.request.urlopen(req_s) as res_s:
            s_data = json.loads(res_s.read().decode("utf-8"))
            found_accounts.extend(s_data.get("results", [])[:3])

    candidate_list = list(dict.fromkeys(top_threats + found_accounts))
    
    accounts_info = []
    for acc in candidate_list:
        try:
            req_p = urllib.request.Request(f"http://127.0.0.1:8000/api/accounts/{acc}")
            with urllib.request.urlopen(req_p) as res_p:
                data = json.loads(res_p.read().decode("utf-8"))
                p = data["profile"]
                r = data["risk_evaluation"]
                
                in_cnt = p.get("incoming_tx_count", 0)
                out_cnt = p.get("outgoing_tx_count", 0)
                total_cnt = in_cnt + out_cnt
                
                if in_cnt > 0 and out_cnt == 0:
                    role_type = "Receiver (Beneficiary / Sink)"
                elif out_cnt > 0 and in_cnt == 0:
                    role_type = "Sender (Origin / Source)"
                elif out_cnt > in_cnt * 2:
                    role_type = "Sender & Receiver (Heavy Outflow / Distributor)"
                elif in_cnt > out_cnt * 2:
                    role_type = "Sender & Receiver (Heavy Inflow / Collector Hub)"
                else:
                    role_type = "Sender & Receiver (Pass-Through Mule)"

                accounts_info.append({
                    "account_number": acc,
                    "role_type": role_type,
                    "inbound_count": in_cnt,
                    "outbound_count": out_cnt,
                    "total_transactions": total_cnt,
                    "total_incoming_inr": p.get("total_incoming", 0),
                    "total_outgoing_inr": p.get("total_outgoing", 0),
                    "risk_score": r.get("mule_risk_score", 0),
                    "risk_category": r.get("risk_category", "UNKNOWN"),
                    "detected_layer": r.get("detected_layer", "NORMAL")
                })
        except Exception as e:
            pass

    return accounts_info

if __name__ == "__main__":
    get_real_accounts()
