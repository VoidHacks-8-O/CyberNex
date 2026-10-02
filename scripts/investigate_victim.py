"""
========================================================================================
OPERATION ABHEDYA-CHAKRA: CLI VICTIM TRACE & BLIND QUERY TOOL
========================================================================================
Usage:
    python scripts/investigate_victim.py --victim V_ACC_1001
    python scripts/investigate_victim.py --victim V_ACC_1001 --hops 4 --generate-reports
========================================================================================
"""

import os
import sys
import argparse
import time

# Add parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.storage.db import DatabaseManager
from backend.graph.trail_engine import MoneyTrailEngine
from backend.evidence.grounding import AntiHallucinationEvidenceEngine
from backend.reports.generator import ForensicReportGenerator
from backend.ai.case_officer import LocalCaseOfficer

def main():
    parser = argparse.ArgumentParser(description="Operation Abhedya-Chakra: 4-Hop Money Trail CLI")
    parser.add_argument("--victim", "-v", required=True, help="Victim Account ID to trace")
    parser.add_argument("--hops", type=int, default=4, help="Maximum traversal hops (default: 4)")
    parser.add_argument("--generate-reports", action="store_true", help="Generate Police Case Diary & Freeze Notice on disk")

    args = parser.parse_args()
    victim_id = args.victim.strip().upper()

    print("\n" + "="*75)
    print(f"[BLIND VICTIM QUERY] Launching 4-Hop Forensic Trace for: {victim_id}")
    print("="*75)

    db = DatabaseManager()
    trail_engine = MoneyTrailEngine(db=db)
    evidence_engine = AntiHallucinationEvidenceEngine(db=db)
    report_gen = ForensicReportGenerator()
    ai_officer = LocalCaseOfficer()

    t0 = time.perf_counter()
    trail_res = trail_engine.trace_victim_trail(victim_id, max_hops=args.hops)
    query_time_ms = (time.perf_counter() - t0) * 1000

    if not trail_res.get("found"):
        print(f"\n[NOT FOUND] {trail_res.get('message')}")
        print("Tip: Run `python scripts/generate_synthetic_data.py` or ingest data first.")
        sys.exit(1)

    print(f"\n[QUERY LATENCY] {query_time_ms:.2f} ms")
    print(f"Total Hops Discovered : {trail_res['total_hops']}")
    print(f"Total Disputed Inflow : Rs. {trail_res['total_disputed_amount']:,.2f}")
    print(f"Total Traced Volume   : Rs. {trail_res['total_trail_volume']:,.2f}")
    print(f"Total Nodes: {len(trail_res['nodes'])} | Total Edges: {len(trail_res['edges'])}")

    print("\n--- IDENTIFIED FORENSIC LAYERS ---")
    print(f"Layer 1 (Collector Mules)    : {', '.join(trail_res['layer_1_collectors']) or 'None'}")
    print(f"Layer 2 (Distributor Mules)  : {', '.join(trail_res['layer_2_distributors']) or 'None'}")
    print(f"Layer 3 (Terminal Cash-Outs) : {', '.join(trail_res['layer_3_terminals']) or 'None'}")

    print("\n--- CHRONOLOGICAL TRANSACTION TRAIL ---")
    for i, e in enumerate(trail_res["edges"], 1):
        print(f"  {i}. [{e['timestamp']}] {e['source']} -> {e['target']} | Rs. {e['amount']:,.2f} | Mode: {e['payment_mode']} | Txn: {e['id']} | Hop {e['hop']}")

    # Grounding and AI Brief
    evidence = evidence_engine.generate_investigation_evidence(trail_res)
    ai_brief = ai_officer.generate_investigative_brief(evidence)

    print("\n--- LOCAL AI CASE OFFICER BRIEFING ---")
    print(ai_brief["incident_summary"])

    if args.generate_reports:
        print("\n--- GENERATING STATUTORY ARTIFACTS ---")
        cd = report_gen.generate_case_diary(trail_res, evidence)
        fn = report_gen.generate_freeze_requisition(trail_res, evidence)
        print(f"  * Police Case Diary saved: {cd['file_path']}")
        print(f"  * Section 91 CrPC Notice saved: {fn['file_path']}")

    print("\n" + "="*75 + "\n")

if __name__ == "__main__":
    main()
