"""
========================================================================================
OPERATION ABHEDYA-CHAKRA: SYNTHETIC FORENSIC BENCHMARK DATASET GENERATOR
========================================================================================
Generates realistic banking transaction datasets for testing and judging demonstrations.
Exhibits:
- Multi-tier money laundering chains (Victim -> L1 Collector -> L2 Distributor -> L3 Terminal)
- High-velocity pass-through (~90% within 3-15 minutes)
- Fan-In and Fan-Out topologies
- Cyber anomalies: Web_Emulator, Linux_Script, P2P/Crypto narration tags, foreign IPs
- Normal background commercial and retail banking traffic
========================================================================================
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def generate_synthetic_cybercrime_dataset(
    n_rows: int = 15_000,
    output_path: str = "data/raw/synthetic_banking_transactions.csv",
    seed: int = 42
) -> str:
    print(f"\n[Data Gen] Synthesizing {n_rows:,} realistic banking transaction records...")
    random.seed(seed)
    np.random.seed(seed)

    base_time = datetime(2026, 9, 1, 9, 0, 0)
    records = []

    # 1. KNOWN LAUNDERING NETWORKS (Ground-Truth rings for demonstration)
    # Ring 1:
    # Victims: V_ACC_1001, V_ACC_1002, V_ACC_1003
    # L1 Collector: C_ACC_5001
    # L2 Distributors: D_ACC_6001, D_ACC_6002
    # L3 Terminals: T_WALLET_7001, T_CRYPTO_7002, T_P2P_7003

    txn_counter = 100000

    # Simulate Ring 1 Flow
    t_curr = base_time + timedelta(hours=10)

    # Inflow to L1 Collector (Fan-In)
    for v_id in ["V_ACC_1001", "V_ACC_1002", "V_ACC_1003", "V_ACC_1004"]:
        amt = random.uniform(85000, 150000)
        t_curr += timedelta(minutes=random.randint(5, 20))
        records.append({
            "Transaction_ID": f"TXN{txn_counter}",
            "Sender_Account": v_id,
            "Receiver_Account": "C_ACC_5001",
            "Sender_IFSC": "SBIN0001234",
            "Receiver_IFSC": "PYTM0123456",
            "Amount": round(amt, 2),
            "Timestamp": t_curr.strftime("%Y-%m-%d %H:%M:%S"),
            "Payment_Mode": "IMPS",
            "Narration": "Payment / transfer [DEMO DATA]",
            "IP_Address": f"103.21.{random.randint(10,99)}.{random.randint(10,250)}",
            "Device_Type": "Android_App"
        })
        txn_counter += 1

    # Rapid Pass-Through from L1 Collector to L2 Distributors (Within 7 minutes)
    t_curr += timedelta(minutes=7)
    for d_id in ["D_ACC_6001", "D_ACC_6002"]:
        records.append({
            "Transaction_ID": f"TXN{txn_counter}",
            "Sender_Account": "C_ACC_5001",
            "Receiver_Account": d_id,
            "Sender_IFSC": "PYTM0123456",
            "Receiver_IFSC": "HDFC0004567",
            "Amount": 210000.00,
            "Timestamp": t_curr.strftime("%Y-%m-%d %H:%M:%S"),
            "Payment_Mode": "RTGS",
            "Narration": "urgent commission settlement [DEMO DATA]",
            "IP_Address": "198.51.100.42",
            "Device_Type": "Web_Emulator"
        })
        txn_counter += 1

    # Dispersal from L2 Distributors to L3 Terminal Cash-Outs (Within 12 minutes)
    t_curr += timedelta(minutes=12)
    for d_id in ["D_ACC_6001", "D_ACC_6002"]:
        for t_id, mode, kw in [
            ("T_WALLET_7001", "WALLET", "wallet topup"),
            ("T_CRYPTO_7002", "CRYPTO", "p2p usdt trade"),
            ("T_P2P_7003", "P2P", "task reward payout")
        ]:
            records.append({
                "Transaction_ID": f"TXN{txn_counter}",
                "Sender_Account": d_id,
                "Receiver_Account": t_id,
                "Sender_IFSC": "HDFC0004567",
                "Receiver_IFSC": "AIRP0009999",
                "Amount": 70000.00,
                "Timestamp": t_curr.strftime("%Y-%m-%d %H:%M:%S"),
                "Payment_Mode": mode,
                "Narration": f"{kw} [DEMO DATA]",
                "IP_Address": "10.0.8.15",
                "Device_Type": "Linux_Script"
            })
            txn_counter += 1

    # 2. Add Background Retail and Commercial Banking Noise
    retail_accounts = [f"ACC_{i:05d}" for i in range(1000, 1000 + max(200, n_rows // 25))]
    modes = ["UPI", "IMPS", "NEFT", "RTGS", "CARD"]
    devices = ["Android_App", "iOS_App", "Web_Portal", "ATM"]
    narrations = ["Grocery", "Salary transfer", "Dinner bill", "Rent", "EMI payment", "Utility recharge"]

    while len(records) < n_rows:
        s_acc = random.choice(retail_accounts)
        r_acc = random.choice(retail_accounts)
        while s_acc == r_acc:
            r_acc = random.choice(retail_accounts)

        t_rand = base_time + timedelta(
            days=random.randint(0, 14),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )

        records.append({
            "Transaction_ID": f"TXN{txn_counter}",
            "Sender_Account": s_acc,
            "Receiver_Account": r_acc,
            "Sender_IFSC": "SBIN0001111",
            "Receiver_IFSC": "ICIC0002222",
            "Amount": round(random.uniform(50, 45000), 2),
            "Timestamp": t_rand.strftime("%Y-%m-%d %H:%M:%S"),
            "Payment_Mode": random.choice(modes),
            "Narration": f"{random.choice(narrations)} [DEMO DATA]",
            "IP_Address": f"49.207.{random.randint(10,99)}.{random.randint(10,250)}",
            "Device_Type": random.choice(devices)
        })
        txn_counter += 1

    df = pd.DataFrame(records)
    # Shuffle so laundering transactions are realistically interspersed
    df = df.sample(frac=1.0, random_state=seed).reset_index(drop=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[Data Gen] Successfully generated {len(df):,} records saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_synthetic_cybercrime_dataset()
