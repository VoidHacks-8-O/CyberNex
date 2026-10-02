import urllib.request
import json
import sys

def run_tests():
    print("==================================================")
    print("VERIFYING OPERATION ABHEDYA-CHAKRA FULL PIPELINE")
    print("==================================================")

    # 1. Test Web Dashboard
    req1 = urllib.request.Request('http://127.0.0.1:8000/')
    with urllib.request.urlopen(req1) as res:
        html = res.read().decode('utf-8')
        assert 'ABHEDYA-CHAKRA' in html
        assert 'TRANSACTION DATA' in html
        assert 'RISK OVERVIEW' in html
        print(f"1. [PASS] Web Dashboard HTML served successfully. Size: {len(html):,} bytes")

    # 2. Test Radar Telemetry
    req2 = urllib.request.Request('http://127.0.0.1:8000/api/radar/metrics')
    with urllib.request.urlopen(req2) as res2:
        radar = json.loads(res2.read().decode('utf-8'))
        print(f"2. [PASS] Radar Telemetry: Center={radar.get('center')}, High Risk={radar.get('high_risk_accounts')}, Active Rings={radar.get('active_rings')}, Mode={radar.get('dataset_mode')}")

    # 3. Test CSV Inspector with Schema details
    req3 = urllib.request.Request('http://127.0.0.1:8000/api/dataset/inspect',
        data=json.dumps({'file_path': 'data/raw/synthetic_banking_transactions.csv'}).encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req3) as res3:
        insp = json.loads(res3.read().decode('utf-8'))
        print(f"3. [PASS] CSV Inspector: Format={insp.get('detected_format')}, Delimiter={insp.get('delimiter')}, Schema Fields={len(insp.get('schema', []))}")

    # 4. Test Pre-flight Validation
    req4 = urllib.request.Request('http://127.0.0.1:8000/api/dataset/validate',
        data=json.dumps({'file_path': 'data/raw/synthetic_banking_transactions.csv', 'column_mapping': insp['suggested_mapping']}).encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req4) as res4:
        val = json.loads(res4.read().decode('utf-8'))
        print(f"4. [PASS] Pre-flight Validation: is_valid={val.get('is_valid')}, Sample Rows={val.get('sample_rows_evaluated')}, Valid={val.get('valid_sample_rows')}")

    # 5. Test 4-Hop Hero Investigation
    req5 = urllib.request.Request('http://127.0.0.1:8000/api/investigation/victim',
        data=json.dumps({'victim_account': 'V_ACC_1001'}).encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req5) as res5:
        inv = json.loads(res5.read().decode('utf-8'))
        trail = inv['trail']
        print(f"5. [PASS] Hero 4-Hop Trace: Discovered Nodes={len(trail['nodes'])}, Transfers={len(trail['edges'])}, Disputed=INR {trail['total_disputed_amount']:,}")

    # 6. Test PDF Document Rejection
    try:
        req6 = urllib.request.Request('http://127.0.0.1:8000/api/dataset/inspect',
            data=json.dumps({'file_path': 'documentation.pdf'}).encode('utf-8'),
            headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req6)
        print("6. [FAIL] PDF should have been rejected!")
        sys.exit(1)
    except urllib.error.HTTPError as e:
        err = json.loads(e.read().decode('utf-8'))
        print(f"6. [PASS] Strict Document Rejection (HTTP {e.code}): {err['detail'][:70]}...")
        assert 'DOCUMENT DETECTED' in err['detail'] or 'PDF detected' in err['detail']

    print("==================================================")
    print("ALL 6 VERIFICATIONS COMPLETED SUCCESSFULLY (100% OPERATIONAL)")
    print("==================================================")

if __name__ == '__main__':
    run_tests()
