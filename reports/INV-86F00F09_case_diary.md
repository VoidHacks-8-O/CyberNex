# 🇮🇳 CYBER CRIME INVESTIGATION WING — POLICE CASE DIARY
### OPERATION ABHEDYA-CHAKRA: FORENSIC TRAIL & MULE RING REPORT
**CONFIDENTIAL // LAW ENFORCEMENT INVESTIGATION RECORD**

---
* **Case / Inquiry ID:** `INV-86F00F09`
* **Date & Time of Generation:** `2026-10-02 03:33:43 IST`
* **Investigating Unit:** `Inspector Vikram Roy`
* **Complainant / Victim Account:** `HDFC10000336`
* **Total Disputed Inflow:** **₹1,160,010.49**
* **Total Downstream Traced Volume:** **₹2,985,324.36**
* **Investigation Depth:** **2 Hops**

---

## 1. EXECUTIVE SUMMARY & LAYER RECONNAISSANCE
The automated forensic graph engine initiated money trail analysis for complainant account `HDFC10000336`.
Illicit outflows were mapped across multi-tier accounts classified under the National Cybercrime Framework:

* **Layer 1 (Collector Mules):** `BARB10000885, BARB10000877, AIRP10000758, PYTM10001081, SBIN10000461, IPOS10000634, IPOS10000989, PUNB10000476, ICIC10000653, HDFC10000882, KKBK10001017, KKBK10000557, BARB10000697, PYTM10000827, BARB10000893`
* **Layer 2 (Distributor Mules):** `SBIN10001276, HDFC10001439, HDFC10001317, ICIC10001399, AIRP10001351, PUNB10001424, IPOS10001103, BARB10001402, PYTM10001387, IPOS10001165, PUNB10001194, BARB10001376, ICIC10001273, PYTM10001321, AXIS10001133, KKBK10001344, AIRP10001291, BARB10001448, AIRP10001293, ICIC10001454, KKBK10001139, ICIC10001226, HDFC10001457, BARB10001132, PYTM10001489, IPOS10001193, PUNB10001374, KKBK10001495, PYTM10001417`
* **Layer 3 (Terminal Cash-Out Nodes):** `None`

---

## 2. CHRONOLOGICAL TRANSACTION TRAIL (DATABASE VERIFIED)
The following transactions represent the exact, time-ordered forensic path of fund dispersion:

| # | Transaction ID | Sender Account | Receiver Account | Amount (INR) | Timestamp | Mode | Narration | Depth |
|---|---|---|---|---|---|---|---|---|
| 1 | `TXN612779475` | `HDFC10000336` | `BARB10000885` | ₹353,665.69 | 2026-09-18 23:50:42 | IMPS | IMPS/P2A/INTERNAL_SETTLEMENT_9970 | Hop 1 |
| 2 | `TXN867821697` | `HDFC10000336` | `BARB10000877` | ₹76,993.94 | 2026-09-18 23:52:19 | IMPS | IMPS/P2A/INTERNAL_SETTLEMENT_5972 | Hop 1 |
| 3 | `TXN283072572` | `HDFC10000336` | `AIRP10000758` | ₹46,545.49 | 2026-09-18 23:53:24 | IMPS | IMPS/P2A/INTERNAL_SETTLEMENT_8160 | Hop 1 |
| 4 | `TXN274804377` | `HDFC10000336` | `PYTM10001081` | ₹39,897.66 | 2026-09-19 15:17:19 | IMPS | IMPS/P2A/INTERNAL_SETTLEMENT_7185 | Hop 1 |
| 5 | `TXN175986213` | `HDFC10000336` | `SBIN10000461` | ₹5,402.67 | 2026-09-19 15:18:51 | IMPS | IMPS/P2A/INTERNAL_SETTLEMENT_9121 | Hop 1 |
| 6 | `TXN226586440` | `HDFC10000336` | `IPOS10000634` | ₹25,675.40 | 2026-09-19 15:20:01 | IMPS | IMPS/P2A/INTERNAL_SETTLEMENT_3086 | Hop 1 |
| 7 | `TXN923099291` | `HDFC10000336` | `IPOS10000989` | ₹1,889.19 | 2026-09-19 15:22:40 | IMPS | IMPS/P2A/INTERNAL_SETTLEMENT_2758 | Hop 1 |
| 8 | `TXN489139019` | `HDFC10000336` | `PUNB10000476` | ₹51,223.77 | 2026-09-20 20:25:27 | IMPS | IMPS/P2A/INTERNAL_SETTLEMENT_6545 | Hop 1 |
| 9 | `TXN112322164` | `HDFC10000336` | `ICIC10000653` | ₹50,239.85 | 2026-09-20 20:27:46 | IMPS | IMPS/P2A/INTERNAL_SETTLEMENT_4460 | Hop 1 |
| 10 | `TXN745545209` | `HDFC10000336` | `HDFC10000882` | ₹360,456.85 | 2026-09-20 20:33:23 | IMPS | IMPS/P2A/INTERNAL_SETTLEMENT_4151 | Hop 1 |
| 11 | `TXN783745779` | `HDFC10000336` | `KKBK10001017` | ₹5,426.74 | 2026-09-20 20:34:45 | IMPS | IMPS/P2A/INTERNAL_SETTLEMENT_8864 | Hop 1 |
| 12 | `TXN838423722` | `HDFC10000336` | `KKBK10000557` | ₹106,948.78 | 2026-09-23 03:20:19 | IMPS | IMPS/P2A/INTERNAL_SETTLEMENT_2363 | Hop 1 |
| 13 | `TXN636156658` | `HDFC10000336` | `BARB10000697` | ₹18,342.06 | 2026-09-23 03:21:15 | IMPS | IMPS/P2A/INTERNAL_SETTLEMENT_1981 | Hop 1 |
| 14 | `TXN248777304` | `HDFC10000336` | `PYTM10000827` | ₹2,318.06 | 2026-09-23 03:22:34 | IMPS | IMPS/P2A/INTERNAL_SETTLEMENT_4901 | Hop 1 |
| 15 | `TXN100453104` | `HDFC10000336` | `BARB10000893` | ₹14,984.34 | 2026-09-23 03:23:02 | IMPS | IMPS/P2A/INTERNAL_SETTLEMENT_2055 | Hop 1 |
| 16 | `TXN722914718` | `BARB10000885` | `SBIN10001276` | ₹339,519.06 | 2026-09-19 00:00:53 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_2724 | Hop 2 |
| 17 | `TXN908775551` | `BARB10000885` | `HDFC10001439` | ₹8,969.41 | 2026-09-22 10:43:38 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_6968 | Hop 2 |
| 18 | `TXN820254509` | `BARB10000877` | `HDFC10001317` | ₹73,914.18 | 2026-09-19 00:17:05 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_3503 | Hop 2 |
| 19 | `TXN860624496` | `AIRP10000758` | `ICIC10001399` | ₹44,683.67 | 2026-09-19 00:13:24 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_3921 | Hop 2 |
| 20 | `TXN446006107` | `PYTM10001081` | `AIRP10001351` | ₹38,301.75 | 2026-09-19 15:38:31 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_1212 | Hop 2 |
| 21 | `TXN764540131` | `PYTM10001081` | `PUNB10001424` | ₹87,172.32 | 2026-09-24 23:22:24 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_1518 | Hop 2 |
| 22 | `TXN747952699` | `SBIN10000461` | `IPOS10001103` | ₹5,186.57 | 2026-09-19 15:47:25 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_8675 | Hop 2 |
| 23 | `TXN911280641` | `IPOS10000634` | `BARB10001402` | ₹24,648.38 | 2026-09-19 15:41:19 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_4047 | Hop 2 |
| 24 | `TXN548345448` | `IPOS10000634` | `PYTM10001387` | ₹10,033.09 | 2026-09-25 18:13:08 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_8611 | Hop 2 |
| 25 | `TXN663192185` | `IPOS10000634` | `IPOS10001165` | ₹40,547.43 | 2026-09-29 11:26:18 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_4848 | Hop 2 |
| 26 | `TXN930570406` | `IPOS10000989` | `PUNB10001194` | ₹1,813.63 | 2026-09-19 15:40:41 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_2526 | Hop 2 |
| 27 | `TXN137277080` | `IPOS10000989` | `BARB10001376` | ₹56,130.76 | 2026-09-22 13:35:49 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_3361 | Hop 2 |
| 28 | `TXN820758102` | `IPOS10000989` | `ICIC10001273` | ₹18,514.20 | 2026-09-23 18:49:11 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_5490 | Hop 2 |
| 29 | `TXN145674028` | `PUNB10000476` | `PYTM10001321` | ₹49,174.81 | 2026-09-20 20:32:58 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_6382 | Hop 2 |
| 30 | `TXN776198372` | `PUNB10000476` | `AXIS10001133` | ₹438.89 | 2026-09-27 07:39:17 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_6031 | Hop 2 |
| 31 | `TXN190226267` | `PUNB10000476` | `KKBK10001344` | ₹39,526.38 | 2026-09-28 15:39:07 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_9276 | Hop 2 |
| 32 | `TXN308260247` | `PUNB10000476` | `AIRP10001291` | ₹30,804.10 | 2026-09-29 09:33:49 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_4848 | Hop 2 |
| 33 | `TXN429290176` | `ICIC10000653` | `BARB10001448` | ₹48,230.25 | 2026-09-20 20:36:38 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_4148 | Hop 2 |
| 34 | `TXN771366100` | `ICIC10000653` | `AIRP10001293` | ₹62,700.41 | 2026-09-24 23:33:36 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_9454 | Hop 2 |
| 35 | `TXN326946084` | `ICIC10000653` | `ICIC10001454` | ₹92,680.97 | 2026-09-28 22:31:04 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_2605 | Hop 2 |
| 36 | `TXN202662450` | `HDFC10000882` | `KKBK10001139` | ₹346,038.57 | 2026-09-20 20:56:47 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_9896 | Hop 2 |
| 37 | `TXN660515013` | `KKBK10001017` | `ICIC10001226` | ₹5,209.67 | 2026-09-20 20:58:31 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_7579 | Hop 2 |
| 38 | `TXN431472416` | `KKBK10001017` | `HDFC10001457` | ₹122,214.41 | 2026-09-24 02:36:10 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_3671 | Hop 2 |
| 39 | `TXN321981939` | `KKBK10000557` | `BARB10001132` | ₹102,670.83 | 2026-09-23 03:27:41 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_5831 | Hop 2 |
| 40 | `TXN933491199` | `KKBK10000557` | `PYTM10001489` | ₹76,438.58 | 2026-09-28 13:22:26 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_8468 | Hop 2 |
| 41 | `TXN838061627` | `BARB10000697` | `IPOS10001193` | ₹17,608.38 | 2026-09-23 03:38:30 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_1448 | Hop 2 |
| 42 | `TXN323429493` | `BARB10000697` | `PUNB10001374` | ₹27,205.73 | 2026-09-23 10:21:04 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_8492 | Hop 2 |
| 43 | `TXN508033743` | `BARB10000697` | `KKBK10001139` | ₹38,327.14 | 2026-09-26 16:04:28 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_7599 | Hop 2 |
| 44 | `TXN876956890` | `PYTM10000827` | `KKBK10001495` | ₹2,225.33 | 2026-09-23 03:28:40 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_6677 | Hop 2 |
| 45 | `TXN992079379` | `BARB10000893` | `PYTM10001417` | ₹14,384.97 | 2026-09-23 03:35:40 | UPI | UPI/WALLET_LOAD/P2P_CRYPTO_5101 | Hop 2 |

---

## 3. SUSPECT MULE ACCOUNTS RECOMMENDED FOR FREEZE REVIEW
Based on composite 0-100 Mule Risk Index scores, fan-in/fan-out patterns, and high-velocity pass-through metrics:

- **Account ID:** `BARB10000885` | **Layer:** `LAYER_1_COLLECTOR` | **Risk Score:** `37.0/100` (MEDIUM)
  *Evidence Grounds:* 96.0% funds dispersed within median 10.2 mins.; Operating from automation/emulator device: Web_Emulator, Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto, settlement
- **Account ID:** `BARB10000877` | **Layer:** `LAYER_1_COLLECTOR` | **Risk Score:** `37.0/100` (MEDIUM)
  *Evidence Grounds:* 96.0% funds dispersed within median 24.8 mins.; Operating from automation/emulator device: Web_Emulator, Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto, settlement
- **Account ID:** `AIRP10000758` | **Layer:** `LAYER_1_COLLECTOR` | **Risk Score:** `37.0/100` (MEDIUM)
  *Evidence Grounds:* 96.0% funds dispersed within median 20.0 mins.; Operating from automation/emulator device: Web_Emulator, Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto, settlement
- **Account ID:** `PYTM10001081` | **Layer:** `LAYER_1_COLLECTOR` | **Risk Score:** `37.0/100` (MEDIUM)
  *Evidence Grounds:* 96.0% funds dispersed within median 16.5 mins.; Operating from automation/emulator device: Web_Emulator, Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto, settlement
- **Account ID:** `SBIN10000461` | **Layer:** `LAYER_1_COLLECTOR` | **Risk Score:** `37.0/100` (MEDIUM)
  *Evidence Grounds:* 96.0% funds dispersed within median 28.6 mins.; Operating from automation/emulator device: Web_Emulator, Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto, settlement
- **Account ID:** `IPOS10000634` | **Layer:** `LAYER_1_COLLECTOR` | **Risk Score:** `37.0/100` (MEDIUM)
  *Evidence Grounds:* 96.0% funds dispersed within median 21.3 mins.; Operating from automation/emulator device: Web_Emulator, Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto, settlement
- **Account ID:** `IPOS10000989` | **Layer:** `LAYER_1_COLLECTOR` | **Risk Score:** `37.0/100` (MEDIUM)
  *Evidence Grounds:* 96.0% funds dispersed within median 18.0 mins.; Operating from automation/emulator device: Web_Emulator, Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto, settlement
- **Account ID:** `PUNB10000476` | **Layer:** `LAYER_1_COLLECTOR` | **Risk Score:** `37.0/100` (MEDIUM)
  *Evidence Grounds:* 96.0% funds dispersed within median 15.0 mins.; Operating from automation/emulator device: Web_Emulator, Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto, settlement
- **Account ID:** `ICIC10000653` | **Layer:** `LAYER_1_COLLECTOR` | **Risk Score:** `37.0/100` (MEDIUM)
  *Evidence Grounds:* 96.0% funds dispersed within median 18.9 mins.; Operating from automation/emulator device: Web_Emulator, Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto, settlement
- **Account ID:** `HDFC10000882` | **Layer:** `LAYER_1_COLLECTOR` | **Risk Score:** `37.0/100` (MEDIUM)
  *Evidence Grounds:* 96.0% funds dispersed within median 23.4 mins.; Operating from automation/emulator device: Web_Emulator, Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto, settlement
- **Account ID:** `KKBK10001017` | **Layer:** `LAYER_1_COLLECTOR` | **Risk Score:** `37.0/100` (MEDIUM)
  *Evidence Grounds:* 96.0% funds dispersed within median 15.8 mins.; Operating from automation/emulator device: Web_Emulator, Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto, settlement
- **Account ID:** `KKBK10000557` | **Layer:** `LAYER_1_COLLECTOR` | **Risk Score:** `37.0/100` (MEDIUM)
  *Evidence Grounds:* 96.0% funds dispersed within median 20.6 mins.; Operating from automation/emulator device: Web_Emulator, Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto, settlement
- **Account ID:** `BARB10000697` | **Layer:** `LAYER_1_COLLECTOR` | **Risk Score:** `37.0/100` (MEDIUM)
  *Evidence Grounds:* 96.0% funds dispersed within median 16.8 mins.; Operating from automation/emulator device: Web_Emulator, Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto, settlement
- **Account ID:** `PYTM10000827` | **Layer:** `LAYER_1_COLLECTOR` | **Risk Score:** `37.0/100` (MEDIUM)
  *Evidence Grounds:* 96.0% funds dispersed within median 12.9 mins.; Operating from automation/emulator device: Web_Emulator, Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto, settlement
- **Account ID:** `BARB10000893` | **Layer:** `LAYER_1_COLLECTOR` | **Risk Score:** `37.0/100` (MEDIUM)
  *Evidence Grounds:* 96.0% funds dispersed within median 12.6 mins.; Operating from automation/emulator device: Web_Emulator, Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto, settlement
- **Account ID:** `SBIN10001276` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 3 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `HDFC10001439` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 7 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `HDFC10001317` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 4 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `PUNB10001424` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 6 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `IPOS10001103` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 4 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `BARB10001402` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 3 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `PYTM10001387` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 6 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `IPOS10001165` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 4 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `PUNB10001194` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 5 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `BARB10001376` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 3 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `ICIC10001273` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 5 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `PYTM10001321` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 4 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `AXIS10001133` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 4 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `KKBK10001344` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 3 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `AIRP10001291` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 3 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `BARB10001448` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 3 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `AIRP10001293` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 4 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `ICIC10001454` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 3 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `KKBK10001139` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 5 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `ICIC10001226` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 4 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `HDFC10001457` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 3 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `BARB10001132` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 4 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `PYTM10001489` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 6 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `IPOS10001193` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 6 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `PUNB10001374` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 6 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `KKBK10001495` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 5 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `PYTM10001417` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `27.0/100` (MEDIUM)
  *Evidence Grounds:* Aggregated funds from 4 distinct senders.; Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `ICIC10001399` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `12.0/100` (LOW)
  *Evidence Grounds:* Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto
- **Account ID:** `AIRP10001351` | **Layer:** `LAYER_2_DISTRIBUTOR` | **Risk Score:** `12.0/100` (LOW)
  *Evidence Grounds:* Operating from automation/emulator device: Linux_Script; Detected illicit/crypto transaction tags: p2p, crypto

---
*Disclaimer: Generated by Operation Abhedya-Chakra Anti-Hallucination Forensics Engine. All transaction IDs, timestamps, and rupee amounts correspond directly to database ground-truth records.*
