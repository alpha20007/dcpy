import csv
import os

# Application Domain: OPD Cardio Appointment System
# RPC/RMI Client-Server Procedure Dispatcher Simulation

CSV_FILENAME = "rpc_calls_265.csv"

class RemoteProcedureDispatcher:
    def __init__(self, domain_name):
        self.domain_name = domain_name

    def processData(self, param):
        val = float(param)
        computed = val * 1.5 + 10.0
        return f"Processed telemetry data {val} -> Result: {computed:.2f} (Committed to {self.domain_name})"

    def validateRecord(self, param):
        return f"Record '{param}' verified successfully in {self.domain_name}"

    def queryStatus(self, param):
        return f"Node '{param}' status: ONLINE (Latency: 12ms)"

    def execute_remote_call(self, method_name, param_value):
        if method_name == "processData":
            return self.processData(param_value)
        elif method_name in ("validateRecord", "validateTransaction", "verifyBlock"):
            return self.validateRecord(param_value)
        elif method_name in ("queryStatus", "queryState", "checkHealth"):
            return self.queryStatus(param_value)
        else:
            return f"Executed default routine '{method_name}' with parameter '{param_value}'"

def load_dataset(filename):
    if os.path.exists(filename):
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            return list(csv.DictReader(file))
    print(f"Dataset '{filename}' not found. Running with default sample data.\n")
    return [
        {"call_id": "101", "client_name": "Client_A", "method_name": "processData", "param_value": "450", "timestamp": "10:00:01"},
        {"call_id": "102", "client_name": "Client_B", "method_name": "validateRecord", "param_value": "TX_8821", "timestamp": "10:00:03"},
        {"call_id": "103", "client_name": "Client_C", "method_name": "processData", "param_value": "620", "timestamp": "10:00:05"},
        {"call_id": "104", "client_name": "Client_D", "method_name": "queryStatus", "param_value": "Worker_Node_4", "timestamp": "10:00:08"},
        {"call_id": "105", "client_name": "Client_E", "method_name": "processData", "param_value": "150", "timestamp": "10:00:12"},
        {"call_id": "106", "client_name": "Client_F", "method_name": "validateRecord", "param_value": "TX_9940", "timestamp": "10:00:15"}
    ]

def main():
    records = load_dataset(CSV_FILENAME)
    dispatcher = RemoteProcedureDispatcher("OPD Cardio Appointment System")

    for row in records:
        call_id = row["call_id"].strip()
        client = row["client_name"].strip()
        method = row["method_name"].strip()
        param = row["param_value"].strip()
        ts = row["timestamp"].strip()

        print(f"[DISPATCH] Client '{client}' invoking method '{method}' (Call ID: {call_id}, Timestamp: {ts})")
        result = dispatcher.execute_remote_call(method, param)
        print(f"[SERVER EXECUTION] Processing parameter '{param}' on procedure '{method}'")
        print(f"[RETURN] {result}")
        print()

if __name__ == "__main__":
    main()

# CSV FILE NAME: rpc_calls_265.csv
# CSV COLUMNS: call_id,client_name,method_name,param_value,timestamp
# COLUMN MEANINGS:
# call_id: Unique identifier for each remote procedure call
# client_name: Identifier of the invoking client node
# method_name: Remote procedure or function to execute on the server
# param_value: Argument value passed into the remote procedure
# timestamp: Timestamp when the call was dispatched
#
# SAMPLE CSV DATA:
# call_id,client_name,method_name,param_value,timestamp
# 101,Client_A,processData,450,10:00:01
# 102,Client_B,validateRecord,TX_8821,10:00:03
# 103,Client_C,processData,620,10:00:05
# 104,Client_D,queryStatus,Worker_Node_4,10:00:08
# 105,Client_E,processData,150,10:00:12
# 106,Client_F,validateRecord,TX_9940,10:00:15
#
# SAVE AS: rpc_calls_265.csv
