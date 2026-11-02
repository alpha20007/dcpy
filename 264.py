import csv
import os

# Application Domain: OPD Cardio Appointment System
# Cristian's Clock Synchronization Algorithm

CSV_FILENAME = "cristian_clocks_264.csv"

def load_dataset(filename):
    if os.path.exists(filename):
        records = []
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                records.append({
                    "client_id": row["client_id"].strip(),
                    "t0_send_ms": float(row["t0_send_ms"].strip()),
                    "t_server_ms": float(row["t_server_ms"].strip()),
                    "t1_recv_ms": float(row["t1_recv_ms"].strip())
                })
        return records
    print(f"Dataset '{filename}' not found. Running with default sample data.\n")
    return [
        {"client_id": "C1", "t0_send_ms": 1000.0, "t_server_ms": 1050.0, "t1_recv_ms": 1100.0},
        {"client_id": "C2", "t0_send_ms": 2000.0, "t_server_ms": 2080.0, "t1_recv_ms": 2120.0},
        {"client_id": "C3", "t0_send_ms": 3000.0, "t_server_ms": 3045.0, "t1_recv_ms": 3070.0},
        {"client_id": "C4", "t0_send_ms": 4000.0, "t_server_ms": 4110.0, "t1_recv_ms": 4180.0},
        {"client_id": "C5", "t0_send_ms": 5000.0, "t_server_ms": 5025.0, "t1_recv_ms": 5060.0},
        {"client_id": "C6", "t0_send_ms": 6000.0, "t_server_ms": 6090.0, "t1_recv_ms": 6140.0}
    ]

def cristians_clock_synchronization(records):
    print("Cristian's Clock Synchronization Computations:\n")
    for row in records:
        cid = row["client_id"]
        t0 = row["t0_send_ms"]
        t_server = row["t_server_ms"]
        t1 = row["t1_recv_ms"]

        rtt = t1 - t0
        estimated_server_time = t_server + (rtt / 2.0)
        clock_offset = estimated_server_time - t1
        adjusted_client_time = t1 + clock_offset

        print(f"Client: {cid}")
        print(f"  Round Trip Time (RTT = T1 - T0): {rtt:.2f} ms")
        print(f"  Estimated Server Time (T_server + RTT/2): {estimated_server_time:.2f} ms")
        print(f"  Local Clock Offset Adjustment: {clock_offset:+.2f} ms")
        print(f"  Adjusted Client Clock: {adjusted_client_time:.2f} ms")
        print()

def main():
    records = load_dataset(CSV_FILENAME)
    cristians_clock_synchronization(records)

if __name__ == "__main__":
    main()

# CSV FILE NAME: cristian_clocks_264.csv
# CSV COLUMNS: client_id,t0_send_ms,t_server_ms,t1_recv_ms
# COLUMN MEANINGS:
# client_id: Unique string identifier for the synchronization client
# t0_send_ms: Client request dispatch timestamp in milliseconds
# t_server_ms: Server receipt and processing timestamp in milliseconds
# t1_recv_ms: Client response receive timestamp in milliseconds
#
# SAMPLE CSV DATA:
# client_id,t0_send_ms,t_server_ms,t1_recv_ms
# C1,1000,1050,1100
# C2,2000,2080,2120
# C3,3000,3045,3070
# C4,4000,4110,4180
# C5,5000,5025,5060
# C6,6000,6090,6140
#
# SAVE AS: cristian_clocks_264.csv
