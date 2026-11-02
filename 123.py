import csv
import os

# Application Domain: Fault-Tolerant Distributed Emulator for Biometric Telemetry
# Lamport's Logical Clock Synchronization and Total Causal Order

CSV_FILENAME = "events_123.csv"

def load_dataset(filename):
    if os.path.exists(filename):
        events = []
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                events.append({
                    "event_id": row["event_id"].strip(),
                    "process_id": row["process_id"].strip(),
                    "event_type": row["event_type"].strip().upper(),
                    "message_to": row["message_to"].strip(),
                    "initial_clock": int(row["initial_clock"].strip())
                })
        return events
    print(f"Dataset '{filename}' not found. Running with default sample data.\n")
    return [
        {"event_id": "E1", "process_id": "P1", "event_type": "SEND", "message_to": "P2", "initial_clock": 0},
        {"event_id": "E2", "process_id": "P2", "event_type": "RECV", "message_to": "P1", "initial_clock": 0},
        {"event_id": "E3", "process_id": "P2", "event_type": "SEND", "message_to": "P3", "initial_clock": 0},
        {"event_id": "E4", "process_id": "P1", "event_type": "INTERNAL", "message_to": "NONE", "initial_clock": 0},
        {"event_id": "E5", "process_id": "P3", "event_type": "RECV", "message_to": "P2", "initial_clock": 0},
        {"event_id": "E6", "process_id": "P3", "event_type": "INTERNAL", "message_to": "NONE", "initial_clock": 0}
    ]

def main():
    events = load_dataset(CSV_FILENAME)
    process_clocks = {"P1": 0, "P2": 0, "P3": 0}
    in_flight_messages = {}
    recorded_events = []

    print("Step-by-step Lamport Clock updates using L = max(L, T_msg) + 1:")
    for ev in events:
        eid = ev["event_id"]
        pid = ev["process_id"]
        etype = ev["event_type"]
        target = ev["message_to"]

        if pid not in process_clocks:
            process_clocks[pid] = ev["initial_clock"]

        old_clock = process_clocks[pid]
        if etype == "INTERNAL":
            process_clocks[pid] += 1
            print(f"  [INTERNAL] Event {eid} on {pid}: L updated from {old_clock} to {process_clocks[pid]}")
        elif etype == "SEND":
            process_clocks[pid] += 1
            in_flight_messages[(pid, target)] = process_clocks[pid]
            print(f"  [SEND] Event {eid} on {pid} -> Target {target}: L updated to {process_clocks[pid]} (Sent T_msg = {process_clocks[pid]})")
        elif etype == "RECV":
            t_msg = in_flight_messages.pop((target, pid), 0)
            process_clocks[pid] = max(process_clocks[pid], t_msg) + 1
            print(f"  [RECV] Event {eid} on {pid} <- Source {target}: L = max({old_clock}, {t_msg}) + 1 = {process_clocks[pid]}")

        recorded_events.append({
            "event_id": eid,
            "process_id": pid,
            "event_type": etype,
            "timestamp": process_clocks[pid]
        })

    sorted_causal_order = sorted(recorded_events, key=lambda x: (x["timestamp"], x["process_id"]))

    print("\nFinal Sorted Total Causal Order of All Events:")
    for rank, ev in enumerate(sorted_causal_order, start=1):
        print(f"  Rank {rank}: Event {ev['event_id']} ({ev['process_id']}, {ev['event_type']}) -> Timestamp: {ev['timestamp']}")

if __name__ == "__main__":
    main()

# CSV FILE NAME: events_123.csv
# CSV COLUMNS: event_id,process_id,event_type,message_to,initial_clock
# COLUMN MEANINGS:
# event_id: Unique event identifier
# process_id: Identifier of the process executing the event (P1/P2/P3)
# event_type: Event category (INTERNAL/SEND/RECV)
# message_to: Recipient process identifier for SEND events, or sender for RECV, or NONE
# initial_clock: Baseline starting logical clock value
#
# SAMPLE CSV DATA:
# event_id,process_id,event_type,message_to,initial_clock
# E1,P1,SEND,P2,0
# E2,P2,RECV,P1,0
# E3,P2,SEND,P3,0
# E4,P1,INTERNAL,NONE,0
# E5,P3,RECV,P2,0
# E6,P3,INTERNAL,NONE,0
#
# SAVE AS: events_123.csv
