import csv
import os

# Application Domain: Distributed Sports Match Synchronization
# Bully Leader Election Algorithm Implementation

CSV_FILENAME = "bully_cluster_220.csv"

class BullyElectionSystem:
    def __init__(self, nodes):
        self.nodes = sorted(nodes, key=lambda n: n["node_id"])
        self.node_map = {n["node_id"]: n for n in self.nodes}

    def run_election(self):
        failed_coordinator = None
        for node in self.nodes:
            if node["is_current_coordinator"] and not node["is_alive"]:
                failed_coordinator = node["node_id"]
                break

        if failed_coordinator is not None:
            print(f"Coordinator failure detected at Node {failed_coordinator}.")
        else:
            print("Coordinator heartbeat check initiated.")

        initiator = None
        for node in self.nodes:
            if node["is_alive"]:
                initiator = node["node_id"]
                break

        if initiator is None:
            print("No active nodes available in cluster for election.")
            return

        print(f"Node {initiator} initiates election.")
        current_candidate = initiator

        while True:
            higher_nodes = [n["node_id"] for n in self.nodes if n["node_id"] > current_candidate and n["is_alive"]]
            all_higher = [n["node_id"] for n in self.nodes if n["node_id"] > current_candidate]

            if not all_higher:
                print(f"Node {current_candidate} has highest ID in cluster. No higher nodes exist.")
                break

            print(f"Node {current_candidate} sending ELECTION to higher nodes: {all_higher}")

            if not higher_nodes:
                print(f"No higher nodes responded to Node {current_candidate}.")
                break

            for h in higher_nodes:
                print(f"Higher Node {h} responding with OK to Node {current_candidate}.")

            current_candidate = max(higher_nodes)

        new_coordinator = current_candidate
        print(f"Node {new_coordinator} elected as new COORDINATOR.")
        print(f"[COORDINATOR] Node {new_coordinator} broadcasting COORDINATOR message to all lower active nodes:")
        for node in self.nodes:
            if node["is_alive"] and node["node_id"] != new_coordinator:
                print(f"  Node {node['node_id']} acknowledged Node {new_coordinator} as COORDINATOR.")
        print(f"Election complete. Active Coordinator: Node {new_coordinator}")

def load_dataset(filename):
    if os.path.exists(filename):
        nodes = []
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                nodes.append({
                    "node_id": int(row["node_id"].strip()),
                    "is_alive": row["is_alive"].strip().upper() == "TRUE",
                    "is_current_coordinator": row["is_current_coordinator"].strip().upper() == "TRUE"
                })
        return nodes
    print(f"Dataset '{filename}' not found. Running with default sample data.\n")
    return [
        {"node_id": 1, "is_alive": True, "is_current_coordinator": False},
        {"node_id": 2, "is_alive": True, "is_current_coordinator": False},
        {"node_id": 3, "is_alive": True, "is_current_coordinator": False},
        {"node_id": 4, "is_alive": True, "is_current_coordinator": False},
        {"node_id": 5, "is_alive": False, "is_current_coordinator": False},
        {"node_id": 6, "is_alive": False, "is_current_coordinator": True}
    ]

def main():
    nodes = load_dataset(CSV_FILENAME)
    system = BullyElectionSystem(nodes)
    system.run_election()

if __name__ == "__main__":
    main()

# CSV FILE NAME: bully_cluster_220.csv
# CSV COLUMNS: node_id,is_alive,is_current_coordinator
# COLUMN MEANINGS:
# node_id: Integer identifier for cluster node
# is_alive: Boolean flag indicating if node is active (TRUE/FALSE)
# is_current_coordinator: Boolean flag indicating if node was the previous coordinator (TRUE/FALSE)
#
# SAMPLE CSV DATA:
# node_id,is_alive,is_current_coordinator
# 1,TRUE,FALSE
# 2,TRUE,FALSE
# 3,TRUE,FALSE
# 4,TRUE,FALSE
# 5,FALSE,FALSE
# 6,FALSE,TRUE
#
# SAVE AS: bully_cluster_220.csv
