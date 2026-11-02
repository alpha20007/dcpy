import csv
import os

# Application Domain: Heterogeneity-Aware Cloud-Edge Load Balancing
# Vector Clocks Implementation and Causal Precedence Analysis

CSV_FILENAME = "vector_events_60.csv"

PROCESSES = ["P1", "P2", "P3"]
PROC_INDEX = {"P1": 0, "P2": 1, "P3": 2}

def compare_vector_clocks(v1, v2):
    less_or_equal = all(x <= y for x, y in zip(v1, v2))
    strictly_less = any(x < y for x, y in zip(v1, v2))
    greater_or_equal = all(x >= y for x, y in zip(v1, v2))
    strictly_greater = any(x > y for x, y in zip(v1, v2))

    if less_or_equal and strictly_less:
        return "Causally Preceding (V1 < V2)"
    elif greater_or_equal and strictly_greater:
        return "Causally Succeeding (V1 > V2)"
    else:
        return "Concurrent (V1 || V2)"

def load_dataset(filename):
    if os.path.exists(filename):
        events = []
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                events.append({
                    "event_id": row["event_id"].strip(),
                    "process_id": row["process_id"].strip(),
                    "event_action": row["event_action"].strip().upper(),
                    "target_process": row["target_process"].strip()
                })
        return events
    print(f"Dataset '{filename}' not found. Running with default sample data.\n")
    return [
        {"event_id": "E1", "process_id": "P1", "event_action": "SEND", "target_process": "P2"},
        {"event_id": "E2", "process_id": "P2", "event_action": "RECV", "target_process": "P1"},
        {"event_id": "E3", "process_id": "P1", "event_action": "INTERNAL", "target_process": "NONE"},
        {"event_id": "E4", "process_id": "P2", "event_action": "SEND", "target_process": "P3"},
        {"event_id": "E5", "process_id": "P3", "event_action": "RECV", "target_process": "P2"},
        {"event_id": "E6", "process_id": "P3", "event_action": "INTERNAL", "target_process": "NONE"}
    ]

def main():
    events = load_dataset(CSV_FILENAME)
    clocks = {p: [0, 0, 0] for p in PROCESSES}
    channel_buffer = {}
    event_clock_records = {}

    print("Step-by-step Vector Clock updates:")
    for ev in events:
        eid = ev["event_id"]
        pid = ev["process_id"]
        action = ev["event_action"]
        target = ev["target_process"]
        p_idx = PROC_INDEX[pid]

        if action == "INTERNAL":
            clocks[pid][p_idx] += 1
        elif action == "SEND":
            clocks[pid][p_idx] += 1
            channel_buffer[(pid, target)] = list(clocks[pid])
        elif action == "RECV":
            clocks[pid][p_idx] += 1
            src_vec = channel_buffer.pop((target, pid), [0, 0, 0])
            for i in range(3):
                clocks[pid][i] = max(clocks[pid][i], src_vec[i])

        event_clock_records[eid] = list(clocks[pid])
        print(f"  Event {eid} ({action} on {pid}): Updated Vector Clock = {clocks[pid]}")

    print("\nCausal Relationship Analysis Between Event Pairs:")
    event_ids = list(event_clock_records.keys())
    for i in range(len(event_ids)):
        for j in range(i + 1, min(i + 3, len(event_ids))):
            e1 = event_ids[i]
            e2 = event_ids[j]
            v1 = event_clock_records[e1]
            v2 = event_clock_records[e2]
            relationship = compare_vector_clocks(v1, v2)
            print(f"  Pair ({e1}, {e2}): {e1}={v1} vs {e2}={v2} -> {relationship}")

if __name__ == "__main__":
    main()

# CSV FILE NAME: vector_events_60.csv
# CSV COLUMNS: event_id,process_id,event_action,target_process
# COLUMN MEANINGS:
# event_id: Unique identifier for the distributed event
# process_id: Identifier of the process where the event occurs (P1/P2/P3)
# event_action: Type of action executed (SEND/RECV/INTERNAL)
# target_process: Communicating process ID or NONE for internal events
#
# SAMPLE CSV DATA:
# event_id,process_id,event_action,target_process
# E1,P1,SEND,P2
# E2,P2,RECV,P1
# E3,P1,INTERNAL,NONE
# E4,P2,SEND,P3
# E5,P3,RECV,P2
# E6,P3,INTERNAL,NONE
#
# SAVE AS: vector_events_60.csv
