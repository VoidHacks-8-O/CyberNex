import os
import sys
import duckdb
import pandas as pd
import json

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.storage.db import DatabaseManager
from backend.ingestion.normalizer import IngestionEngine

def test_isolated_lifecycle():
    print("=" * 80)
    print("STEP 1: TESTING ISOLATED DUCKDB & INGESTION LIFECYCLE (TEMP DB)")
    print("=" * 80)

    temp_db_path = os.path.join(os.getcwd(), "data", "processed", "temp_test_abhedya.duckdb")
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)

    db = DatabaseManager(db_path=temp_db_path)
    
    # 1. Check initial empty state
    stats = db.get_dataset_stats()
    print("Initial Empty Stats:", stats)
    assert stats["total_transactions"] == 0
    assert stats["dataset_mode"] == "NO_DATA"
    assert stats["dataset_loaded"] is False

    # 2. Create a small test CSV (10 rows)
    test_csv_path = os.path.join(os.getcwd(), "data", "raw", "small_test_sample.csv")
    test_df = pd.DataFrame([
        {
            "Transaction_ID": f"TEST_TX_{i:04d}",
            "Sender_Account": f"ACC_SRC_{i:02d}",
            "Receiver_Account": f"ACC_DST_{i:02d}",
            "Sender_IFSC": "HDFC0001234",
            "Receiver_IFSC": "SBIN0005678",
            "Amount": 1000.0 * (i + 1),
            "Timestamp": "2026-09-20 10:00:00",
            "Payment_Mode": "IMPS",
            "Narration": "TEST TRANSFER",
            "IP_Address": "192.168.1.1",
            "Device_Type": "Mobile_App"
        }
        for i in range(10)
    ])
    test_df.to_csv(test_csv_path, index=False)
    print(f"Created small test CSV with {len(test_df)} rows at {test_csv_path}")

    # 3. Ingest the small test CSV
    ingestor = IngestionEngine()
    ingestor.db = db
    summary = ingestor.ingest_file(test_csv_path, clear_existing=True)
    print("Ingestion Summary:", summary)
    assert summary["valid_rows_stored"] == 10
    assert summary["status"] == "READY"

    # 4. Check status after ingestion
    stats_after = db.get_dataset_stats()
    print("Stats After Ingestion:", stats_after)
    assert stats_after["total_transactions"] == 10
    assert stats_after["dataset_loaded"] is True
    assert stats_after["dataset_filename"] == "small_test_sample.csv"

    # 5. Test investigation
    res = db.resolve_identifier("TEST_TX_0001")
    print("Resolve TEST_TX_0001:", res)
    assert res["found"] is True
    assert res["is_transaction"] is True

    # 6. Test Reset Database
    print("\nExecuting db.reset_database()...")
    reset_ok = db.reset_database()
    assert reset_ok is True

    stats_reset = db.get_dataset_stats()
    print("Stats After Reset:", stats_reset)
    assert stats_reset["total_transactions"] == 0
    assert stats_reset["dataset_loaded"] is False
    assert stats_reset["dataset_mode"] == "NO_DATA"
    assert stats_reset["dataset_filename"] == "None"

    # Verify resolution after reset returns not found
    res_after_reset = db.resolve_identifier("TEST_TX_0001")
    print("Resolve TEST_TX_0001 After Reset:", res_after_reset)
    assert res_after_reset["found"] is False

    # Clean up temp files
    db.close()
    if os.path.exists(temp_db_path):
        try:
            os.remove(temp_db_path)
        except Exception:
            pass
    if os.path.exists(test_csv_path):
        os.remove(test_csv_path)

    print("\n[PASS] Isolated DuckDB Lifecycle Test Passed 100%!")

if __name__ == "__main__":
    test_isolated_lifecycle()
