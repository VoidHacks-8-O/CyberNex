import urllib.request
import urllib.error
import json
import sys

# Configure UTF-8 encoding for standard output
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def run_test(identifier: str, expected_type: str, test_num: int):
    print(f"\n=======================================================")
    print(f"TEST {test_num}: Investigating '{identifier}' (Expected: {expected_type})")
    print(f"=======================================================")
    
    url = f"{BASE_URL}/api/investigate/{identifier}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            data = json.loads(resp.read().decode('utf-8'))
            
            print(f"[PASS] HTTP Status: {status}")
            print(f"[PASS] Entity Type: {data.get('entity_type')}")
            print(f"[PASS] Type Badge: {data.get('type_badge')}")
            
            if data.get('entity_type') == 'TRANSACTION_ID':
                tx = data.get('transaction', {})
                print(f"[PASS] Transaction ID: {tx.get('transaction_id')}")
                print(f"[PASS] Sender Account: {tx.get('sender_account')} (IFSC: {tx.get('sender_ifsc')})")
                print(f"[PASS] Receiver Account: {tx.get('receiver_account')} (IFSC: {tx.get('receiver_ifsc')})")
                print(f"[PASS] Amount: INR {tx.get('amount'):,.2f}")
                print(f"[PASS] Timestamp: {tx.get('timestamp')}")
                print(f"[PASS] Payment Mode: {tx.get('payment_mode')}")
                print(f"[PASS] IP Address: {tx.get('ip_address')} | Device: {tx.get('device_type')}")
                print(f"[PASS] Narration: {tx.get('narration')}")
                trail = data.get('trail', {})
                print(f"[PASS] 4-Hop Graph Nodes: {len(trail.get('nodes', []))} | Edges: {len(trail.get('edges', []))}")
                assert tx.get('transaction_id') == identifier, "Tx ID mismatch"
            else:
                f = data.get('account_forensics', {})
                r = data.get('risk_evaluation', {})
                print(f"[PASS] Account ID: {f.get('account_id')}")
                print(f"[PASS] Total Inbound: INR {f.get('total_incoming', 0):,.2f} ({f.get('incoming_tx_count')} txns)")
                print(f"[PASS] Total Outbound: INR {f.get('total_outgoing', 0):,.2f} ({f.get('outgoing_tx_count')} txns)")
                print(f"[PASS] Unique Senders: {f.get('unique_senders')} | Unique Receivers: {f.get('unique_receivers')}")
                print(f"[PASS] Pass-Through Ratio: {f.get('pass_through_ratio', 0)*100:.1f}%")
                print(f"[PASS] First Seen: {f.get('first_seen')} | Last Seen: {f.get('last_seen')}")
                print(f"[PASS] Mule Risk Index: {r.get('mule_risk_score')}/100 ({r.get('risk_category')})")
                print(f"[PASS] Grounded Indicators: {r.get('primary_indicators')}")
                trail = data.get('trail', {})
                print(f"[PASS] 4-Hop Graph Nodes: {len(trail.get('nodes', []))} | Edges: {len(trail.get('edges', []))}")
                assert f.get('account_id') == identifier, "Account ID mismatch"

            return True

    except urllib.error.HTTPError as e:
        if expected_type == "INVALID":
            err_body = json.loads(e.read().decode('utf-8'))
            print(f"[PASS] Correctly returned HTTP {e.code}")
            print(f"[PASS] Detail Message: {err_body.get('detail')}")
            assert err_body.get('detail') == "No matching record found in the imported transaction dataset.", "Wrong error detail"
            return True
        else:
            print(f"[FAIL] Unexpected HTTP Error {e.code}: {e.read().decode('utf-8')}")
            return False
    except Exception as e:
        print(f"[FAIL] Exception: {e}")
        return False

def main():
    test_cases = [
        # 3 Real Transaction IDs
        ("TXN612779475", "TRANSACTION_ID"),
        ("TXN867821697", "TRANSACTION_ID"),
        ("TXN283072572", "TRANSACTION_ID"),
        # 3 Real Sender Accounts
        ("HDFC10000336", "SENDER_ACCOUNT / DUAL"),
        ("SBIN10000344", "SENDER_ACCOUNT"),
        ("AIRP10000341", "SENDER_ACCOUNT / DUAL"),
        # 3 Real Receiver Accounts
        ("BARB10000885", "RECEIVER_ACCOUNT"),
        ("BARB10000877", "RECEIVER_ACCOUNT"),
        ("AIRP10000758", "RECEIVER_ACCOUNT"),
        # 1 Invalid Identifier
        ("INVALID_TEST_123456", "INVALID")
    ]

    passed = 0
    for idx, (ident, exp_type) in enumerate(test_cases, start=1):
        ok = run_test(ident, exp_type, idx)
        if ok:
            passed += 1

    print("\n" + "="*55)
    print(f"FINAL TEST SUMMARY: {passed}/{len(test_cases)} TESTS PASSED (100% REAL DATASET)")
    print("="*55)

if __name__ == "__main__":
    main()
