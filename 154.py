import csv
import os

# Application Domain: Distributed Online Quiz System
# Berkeley Physical Clock Synchronization Algorithm

CSV_FILENAME = "node_clocks_154.csv"

def load_dataset(filename):
    if os.path.exists(filename):
        nodes = []
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                nodes.append({
                    "node_id": row["node_id"].strip(),
                    "clock_time_sec": float(row["clock_time_sec"].strip()),
                    "is_faulty": row["is_faulty"].strip().upper() == "TRUE"
                })
        return nodes
    print(f"Dataset '{filename}' not found. Running with default sample data.\n")
    return [
        {"node_id": "N1", "clock_time_sec": 3600.0, "is_faulty": False},
        {"node_id": "N2", "clock_time_sec": 3605.0, "is_faulty": False},
        {"node_id": "N3", "clock_time_sec": 3595.0, "is_faulty": False},
        {"node_id": "N4", "clock_time_sec": 3980.0, "is_faulty": True},
        {"node_id": "N5", "clock_time_sec": 3602.0, "is_faulty": False},
        {"node_id": "N6", "clock_time_sec": 3598.0, "is_faulty": False}
    ]

def berkeley_synchronization(nodes):
    print("Polled node clock times:")
    for node in nodes:
        print(f"  Node {node['node_id']}: {node['clock_time_sec']:.1f}s (Faulty Flag: {node['is_faulty']})")

    valid_nodes = []
    discarded_nodes = []

    for node in nodes:
        if node["is_faulty"]:
            discarded_nodes.append((node["node_id"], node["clock_time_sec"], "Flagged Faulty"))
        else:
            valid_nodes.append(node)

    if valid_nodes:
        times = [n["clock_time_sec"] for n in valid_nodes]
        median_time = sorted(times)[len(times) // 2]
        threshold = 60.0
        filtered_valid = []
        for n in valid_nodes:
            if abs(n["clock_time_sec"] - median_time) > threshold:
                discarded_nodes.append((n["node_id"], n["clock_time_sec"], "Outlier Deviation"))
            else:
                filtered_valid.append(n)
        valid_nodes = filtered_valid

    print()
    print("Identified and discarded faulty / outlier nodes:")
    if discarded_nodes:
        for node_id, t, reason in discarded_nodes:
            print(f"  Discarded Node {node_id}: {t:.1f}s (Reason: {reason})")
    else:
        print("  None")

    if not valid_nodes:
        print("Error: No valid nodes remaining for time averaging.")
        return

    avg_time = sum(n["clock_time_sec"] for n in valid_nodes) / len(valid_nodes)
    print(f"\nCalculated average synchronized time: {avg_time:.2f}s")
    print("\nRelative adjustments per node:")
    for node in nodes:
        node_time = node["clock_time_sec"]
        if any(node["node_id"] == v["node_id"] for v in valid_nodes):
            adj = avg_time - node_time
            synced = node_time + adj
            print(f"  Node {node['node_id']}: Adjustment = {adj:+.2f}s -> Synchronized Clock = {synced:.2f}s")
        else:
            print(f"  Node {node['node_id']}: Faulty/Outlier - Clock reset to synchronized average {avg_time:.2f}s")

def main():
    nodes = load_dataset(CSV_FILENAME)
    berkeley_synchronization(nodes)

if __name__ == "__main__":
    main()

# CSV FILE NAME: node_clocks_154.csv
# CSV COLUMNS: node_id,clock_time_sec,is_faulty
# COLUMN MEANINGS:
# node_id: Unique string identifier for node
# clock_time_sec: Local clock reading of node in seconds
# is_faulty: Boolean indicating if node clock is faulty or outlier (TRUE/FALSE)
#
# SAMPLE CSV DATA:
# node_id,clock_time_sec,is_faulty
# N1,3600,FALSE
# N2,3605,FALSE
# N3,3595,FALSE
# N4,3980,TRUE
# N5,3602,FALSE
# N6,3598,FALSE
#
# SAVE AS: node_clocks_154.csv
