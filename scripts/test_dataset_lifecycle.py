import urllib.request
import urllib.error
import json
import time
import os
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

def make_req(endpoint, method="GET", body=None, origin="http://127.0.0.1:8000"):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if origin:
        headers["Origin"] = origin
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))

def run_regression():
    print("=" * 80)
    print("DATASET RESET & LIFECYCLE REGRESSION TEST SUITE")
    print("=" * 80)

    # 1. Check Status Before Reset
    print("\n--- TEST 1: Initial Dataset Status ---")
    st, res = make_req("/api/dataset/status", origin="null")
    print(f"Status ({st}): total_txns={res['dataset_statistics']['total_transactions']}, mode={res['dataset_statistics']['dataset_mode']}, file={res['dataset_statistics']['dataset_filename']}")

    # 2. Perform Database Reset
    print("\n--- TEST 2: Execute Database Reset (POST /api/dataset/reset) ---")
    st, res = make_req("/api/dataset/reset", method="POST", origin="null")
    print(f"Reset Response ({st}):", res)
    assert st == 200
    assert res["status"] == "SUCCESS"

    # 3. Check Status Immediately After Reset (Both origins: null and http)
    print("\n--- TEST 3: Verify Empty State (file:// and http://) ---")
    st1, res1 = make_req("/api/dataset/status", origin="null")
    st2, res2 = make_req("/api/dataset/status", origin="http://127.0.0.1:8000")
    print("file:// Origin Status:", res1['dataset_statistics'])
    print("http:// Origin Status:", res2['dataset_statistics'])
    assert res1['dataset_statistics']['total_transactions'] == 0
    assert res1['dataset_statistics']['dataset_loaded'] is False
    assert res1['dataset_statistics']['dataset_mode'] == "NO_DATA"

    # 4. Check Radar Metrics & Dynamic Chips After Reset
    print("\n--- TEST 4: Verify Radar & Chips in Empty State ---")
    st_r, res_r = make_req("/api/radar/metrics", origin="null")
    st_c, res_c = make_req("/api/dataset/sample-chips", origin="null")
    print(f"Radar ({st_r}): total_transactions={res_r.get('total_transactions')}, top_threats count={len(res_r.get('top_threats', []))}")
    print(f"Chips ({st_c}): count={len(res_c.get('chips', []))}")
    assert res_r.get('total_transactions') == 0
    assert len(res_r.get('top_threats', [])) == 0
    assert len(res_c.get('chips', [])) == 0

    # 5. Create Small Test CSV (15 rows)
    test_csv_path = os.path.abspath("data/raw/custom_replacement_test.csv")
    test_data = [
        {
            "Transaction_ID": f"NEW_TXN_{i:03d}",
            "Sender_Account": f"NEW_SENDER_{i:02d}",
            "Receiver_Account": f"NEW_RECEIVER_{i:02d}",
            "Sender_IFSC": "HDFC0001000",
            "Receiver_IFSC": "SBIN0002000",
            "Amount": 5000.0 * (i + 1),
            "Timestamp": "2026-10-01 12:00:00",
            "Payment_Mode": "UPI",
            "Narration": "NEW DATASET TRANSACTION",
            "IP_Address": "10.0.0.1",
            "Device_Type": "Android"
        }
        for i in range(15)
    ]
    pd.DataFrame(test_data).to_csv(test_csv_path, index=False)
    print(f"\n--- TEST 5: Created Small Replacement CSV (15 rows): {test_csv_path} ---")

    # 6. Ingest Small Replacement CSV
    print("\n--- TEST 6: Ingesting Small Replacement Dataset ---")
    st_ing, res_ing = make_req("/api/dataset/start-ingestion", method="POST", body={
        "file_path": test_csv_path,
        "is_demo": False
    }, origin="null")
    print(f"Start Ingestion ({st_ing}):", res_ing)

    # Poll until ready
    for _ in range(30):
        time.sleep(0.5)
        st_p, res_p = make_req("/api/dataset/progress", origin="null")
        if res_p.get("status") == "READY":
            print("Ingestion Finished with Status READY! Summary:", res_p.get("last_summary"))
            break

    # 7. Check Status After Small Dataset Ingested
    print("\n--- TEST 7: Verify Status for New Dataset ---")
    st_new, res_new = make_req("/api/dataset/status", origin="null")
    print("New Dataset Stats:", res_new['dataset_statistics'])
    assert res_new['dataset_statistics']['total_transactions'] == 15
    assert res_new['dataset_statistics']['dataset_loaded'] is True
    assert res_new['dataset_statistics']['dataset_filename'] == "custom_replacement_test.csv"

    # 8. Investigation on New Dataset
    print("\n--- TEST 8: Investigation on New Dataset Identifier (NEW_TXN_005) ---")
    st_inv, res_inv = make_req("/api/investigation/universal", method="POST", body={"identifier": "NEW_TXN_005"}, origin="null")
    print(f"Investigation Status ({st_inv}):", res_inv.get("entity_type"), "| Tx ID:", res_inv.get("transaction", {}).get("transaction_id"))
    assert st_inv == 200
    assert res_inv.get("transaction", {}).get("transaction_id") == "NEW_TXN_005"

    # 9. Verify Old Dataset Identifier Is NOT Found
    print("\n--- TEST 9: Verify Old Identifier (TXN401119292) is NOT in New Dataset ---")
    st_old, res_old = make_req("/api/investigation/universal", method="POST", body={"identifier": "TXN401119292"}, origin="null")
    print(f"Old ID Status ({st_old}):", res_old.get("detail"))
    assert st_old == 404

    # 10. Clean up test file
    if os.path.exists(test_csv_path):
        os.remove(test_csv_path)

    print("\n" + "=" * 80)
    print("ALL 10 DATASET RESET & REPLACEMENT LIFECYCLE TESTS PASSED 100%!")
    print("=" * 80)

if __name__ == "__main__":
    run_regression()
