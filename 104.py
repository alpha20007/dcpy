import csv
import os

# Application Domain: Distributed Railway Signal Coordination
# Ring Leader Election Algorithm Implementation

CSV_FILENAME = "ring_nodes_104.csv"

class RingElectionSystem:
    def __init__(self, nodes):
        self.nodes = sorted(nodes, key=lambda n: n["node_id"])
        self.node_map = {n["node_id"]: n for n in self.nodes}

    def get_next_active_node(self, current_id):
        curr = self.node_map[current_id]
        nxt_id = curr["next_node_id"]
        while nxt_id in self.node_map:
            if self.node_map[nxt_id]["is_active"]:
                return nxt_id
            nxt_id = self.node_map[nxt_id]["next_node_id"]
            if nxt_id == current_id:
                break
        return None

    def run_election(self):
        failed_coordinator = None
        for n in self.nodes:
            if not n["is_active"] and n["priority_rank"] == max(item["priority_rank"] for item in self.nodes):
                failed_coordinator = n["node_id"]
                break

        if failed_coordinator is not None:
            print(f"Detected failure of coordinator at Node {failed_coordinator}.")
        else:
            print("Coordinator failure detected in active ring heartbeat.")

        active_nodes = [n for n in self.nodes if n["is_active"]]
        if not active_nodes:
            print("Error: No active nodes remaining in the ring.")
            return

        initiator = active_nodes[0]["node_id"]
        print(f"Node {initiator} initiates election token circulation.\n")

        token_list = [initiator]
        current_node = initiator

        while True:
            next_node = self.get_next_active_node(current_node)
            if next_node is None or next_node == initiator:
                print(f"Token message circulating: Node {current_node} passes final token {token_list} back to Initiator Node {initiator}.")
                break

            token_list.append(next_node)
            print(f"Token message circulating: Node {current_node} passes token {token_list} to Node {next_node}.")
            current_node = next_node

        elected_leader = max(token_list, key=lambda nid: (self.node_map[nid]["priority_rank"], nid))
        print(f"\nToken completed full cycle across all active ring nodes.")
        print(f"Final election result: Node {elected_leader} elected as COORDINATOR (Priority Rank: {self.node_map[elected_leader]['priority_rank']}).")
        print(f"Node {elected_leader} broadcasting COORDINATOR announcement token along the ring.")

def load_dataset(filename):
    if os.path.exists(filename):
        nodes = []
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                nodes.append({
                    "node_id": int(row["node_id"].strip()),
                    "next_node_id": int(row["next_node_id"].strip()),
                    "is_active": row["is_active"].strip().upper() == "TRUE",
                    "priority_rank": int(row["priority_rank"].strip())
                })
        return nodes
    print(f"Dataset '{filename}' not found. Running with default sample data.\n")
    return [
        {"node_id": 1, "next_node_id": 2, "is_active": True, "priority_rank": 40},
        {"node_id": 2, "next_node_id": 3, "is_active": True, "priority_rank": 65},
        {"node_id": 3, "next_node_id": 4, "is_active": True, "priority_rank": 80},
        {"node_id": 4, "next_node_id": 5, "is_active": True, "priority_rank": 95},
        {"node_id": 5, "next_node_id": 6, "is_active": False, "priority_rank": 100},
        {"node_id": 6, "next_node_id": 1, "is_active": True, "priority_rank": 70}
    ]

def main():
    nodes = load_dataset(CSV_FILENAME)
    ring_system = RingElectionSystem(nodes)
    ring_system.run_election()

if __name__ == "__main__":
    main()

# CSV FILE NAME: ring_nodes_104.csv
# CSV COLUMNS: node_id,next_node_id,is_active,priority_rank
# COLUMN MEANINGS:
# node_id: Unique integer identifier for current ring node
# next_node_id: Integer identifier of successor node in the directed ring
# is_active: Boolean indicating if node is operational (TRUE/FALSE)
# priority_rank: Integer priority weighting used during leader election
#
# SAMPLE CSV DATA:
# node_id,next_node_id,is_active,priority_rank
# 1,2,TRUE,40
# 2,3,TRUE,65
# 3,4,TRUE,80
# 4,5,TRUE,95
# 5,6,FALSE,100
# 6,1,TRUE,70
#
# SAVE AS: ring_nodes_104.csv
