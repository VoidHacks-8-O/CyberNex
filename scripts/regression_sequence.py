import urllib.request
import urllib.error
import json
import time

seq = [
    ("TXN401119292", 200, True),
    ("KKBK10000000", 200, True),
    ("ICIC10000335", 200, True),
    ("TXN401119292", 200, True),
    ("INVALID_TEST_99999", 404, False),
    ("KKBK10000000", 200, True)
]

print("=" * 70)
print("EXECUTING 6-STEP REGRESSION SEQUENCE (WITHOUT PAGE RELOAD)")
print("=" * 70)

for idx, (ident, exp_status, exp_found) in enumerate(seq, 1):
    t0 = time.time()
    url = f"http://127.0.0.1:8000/api/investigate/{ident}"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as resp:
            elapsed = time.time() - t0
            data = json.loads(resp.read().decode("utf-8"))
            entity_type = data.get('entity_type')
            nodes = len(data.get('trail', {}).get('nodes', []))
            print(f"Step {idx}: '{ident}' -> HTTP {resp.status} | found: True | entity_type: {entity_type} | nodes: {nodes} | time: {elapsed:.2f}s")
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        err_body = json.loads(e.read().decode("utf-8"))
        print(f"Step {idx}: '{ident}' -> HTTP {e.code} | found: False | detail: '{err_body.get('detail')}' | time: {elapsed:.2f}s")

print("=" * 70)
