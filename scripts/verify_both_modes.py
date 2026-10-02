import urllib.request
import json
import time

def test_identifier(ident, mode_name, origin_header):
    t0 = time.time()
    url = "http://127.0.0.1:8000/api/investigation/universal"
    headers = {"Content-Type": "application/json"}
    if origin_header:
        headers["Origin"] = origin_header

    req = urllib.request.Request(url, data=json.dumps({"identifier": ident, "max_hops": 4}).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req) as resp:
        elapsed = time.time() - t0
        data = json.loads(resp.read().decode("utf-8"))
        cors = resp.headers.get("Access-Control-Allow-Origin")
        nodes = len(data.get("trail", {}).get("nodes", []))
        edges = len(data.get("trail", {}).get("edges", []))
        print(f"[{mode_name}] ID: {ident:15} | Status: {resp.status} | CORS: {cors} | Type: {data.get('entity_type'):15} | Nodes: {nodes:2} | Edges: {edges:2} | Time: {elapsed:.2f}s")

print("=" * 80)
print("TEST A: HTTP SERVED MODE (http://127.0.0.1:8000/)")
print("=" * 80)
test_identifier("TXN401119292", "HTTP-SERVED", "http://127.0.0.1:8000")
test_identifier("KKBK10000000", "HTTP-SERVED", "http://127.0.0.1:8000")
test_identifier("ICIC10000335", "HTTP-SERVED", "http://127.0.0.1:8000")

print("\n" + "=" * 80)
print("TEST B: DIRECT FILE MODE (file:///.../frontend/index.html)")
print("=" * 80)
test_identifier("TXN401119292", "DIRECT-FILE", "null")
test_identifier("KKBK10000000", "DIRECT-FILE", "null")
test_identifier("ICIC10000335", "DIRECT-FILE", "null")

print("\n" + "=" * 80)
print("CONSECUTIVE SEARCHES WITHOUT RELOAD (Simulating multiple button clicks)")
print("=" * 80)
test_identifier("TXN401119292", "CLICK-1", "null")
test_identifier("KKBK10000000", "CLICK-2", "null")
test_identifier("ICIC10000335", "CLICK-3", "null")
test_identifier("TXN401119292", "CLICK-4", "null")
print("=" * 80)
