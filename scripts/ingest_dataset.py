"""
========================================================================================
OPERATION ABHEDYA-CHAKRA: CLI DATASET INGESTION COMMAND
========================================================================================
Usage:
    python scripts/ingest_dataset.py --file path/to/dataset.csv
    python scripts/ingest_dataset.py --file path/to/dataset.parquet --chunk-size 100000
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

from backend.ingestion.normalizer import IngestionEngine
from backend.storage.db import DatabaseManager

def main():
    parser = argparse.ArgumentParser(description="Operation Abhedya-Chakra: High-Throughput Ingestion CLI")
    parser.add_argument("--file", "-f", required=True, help="Path to raw CSV, CSV.GZ, or Parquet dataset")
    parser.add_argument("--chunk-size", "-c", type=int, default=50000, help="Chunk size for streaming processing")
    parser.add_argument("--reset-db", action="store_true", help="Clear existing database before ingesting")

    args = parser.parse_args()
    file_path = os.path.abspath(args.file)

    if not os.path.exists(file_path):
        print(f"[ERROR] Specified file not found: {file_path}")
        sys.exit(1)

    print("\n" + "="*75)
    print(f"[INGESTION] Ingesting Dataset: {file_path}")
    print(f"Chunk Size: {args.chunk_size:,} rows | Reset DB: {args.reset_db}")
    print("="*75)

    db = DatabaseManager()
    if args.reset_db:
        print("[INFO] Resetting database tables...")
        db.reset_database()

    ingestor = IngestionEngine()

    def progress_callback(info):
        if info.get("status") == "INGESTING":
            print(f"  * Processed: {info['rows_processed']:,} rows | Valid: {info['valid_rows']:,} | Speed: {info['rows_per_sec']:,.0f} rows/s", end="\r")
        elif info.get("status") == "INDEXING":
            print(f"\n  * {info.get('message')}")

    t0 = time.time()
    summary = ingestor.ingest_file(file_path, chunk_size=args.chunk_size, progress_callback=progress_callback)
    total_time = time.time() - t0

    print("\n" + "="*75)
    print("[SUCCESS] Ingestion and B-Tree Indexing Complete!")
    print(f"  * Total Rows Processed : {summary['total_rows_read']:,}")
    print(f"  * Valid Records Stored : {summary['valid_rows_stored']:,}")
    print(f"  * Rejected Records     : {summary['rejected_rows']:,}")
    print(f"  * Unique Accounts      : {summary['unique_accounts']:,}")
    print(f"  * Total Transacted Vol : Rs. {summary['total_volume_inr']:,.2f}")
    print(f"  * Total Duration       : {total_time:.2f} seconds")
    print(f"  * Overall Throughput   : {summary['throughput_rows_sec']:,.0f} rows/sec")
    print("="*75 + "\n")

if __name__ == "__main__":
    main()
