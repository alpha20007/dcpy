import csv
import os

# Application Domain: Distributed E-Voting System
# Dynamic Workload Scheduling / Load Balancing Simulation

CSV_FILENAME = "workload_308.csv"

def load_dataset(filename):
    if os.path.exists(filename):
        jobs = []
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                jobs.append({
                    "job_id": row["job_id"].strip(),
                    "compute_units": float(row["compute_units"].strip()),
                    "assigned_worker": row["assigned_worker"].strip(),
                    "status": row["status"].strip()
                })
        return jobs
    print(f"Dataset '{filename}' not found. Running with default sample data.\n")
    return [
        {"job_id": "J101", "compute_units": 35.0, "assigned_worker": "UNASSIGNED", "status": "PENDING"},
        {"job_id": "J102", "compute_units": 50.0, "assigned_worker": "UNASSIGNED", "status": "PENDING"},
        {"job_id": "J103", "compute_units": 20.0, "assigned_worker": "UNASSIGNED", "status": "PENDING"},
        {"job_id": "J104", "compute_units": 75.0, "assigned_worker": "UNASSIGNED", "status": "PENDING"},
        {"job_id": "J105", "compute_units": 40.0, "assigned_worker": "UNASSIGNED", "status": "PENDING"},
        {"job_id": "J106", "compute_units": 60.0, "assigned_worker": "UNASSIGNED", "status": "PENDING"}
    ]

def dynamic_load_balancing(jobs, workers):
    worker_loads = {w: 0.0 for w in workers}
    worker_tasks = {w: [] for w in workers}

    print("Incoming job allocations (Least-Connections / Least-Loaded Dynamic Strategy):")
    for job in jobs:
        selected_worker = min(workers, key=lambda w: worker_loads[w])
        worker_loads[selected_worker] += job["compute_units"]
        worker_tasks[selected_worker].append(job["job_id"])
        job["assigned_worker"] = selected_worker
        job["status"] = "ASSIGNED"

        print(f"  [ALLOCATION] Job {job['job_id']} ({job['compute_units']:.0f} compute units) -> Assigned to {selected_worker} | Current Load of {selected_worker}: {worker_loads[selected_worker]:.0f}")

    total_load = sum(worker_loads.values())
    avg_load = total_load / len(workers) if workers else 0.0

    print("\nBalanced Summary of Tasks Across All Worker Nodes:")
    for w in workers:
        pct = (worker_loads[w] / total_load * 100.0) if total_load > 0 else 0.0
        print(f"  Worker: {w:10} | Assigned Jobs: {len(worker_tasks[w]):2} {str(worker_tasks[w]):24} | Total Load: {worker_loads[w]:6.1f} units ({pct:5.1f}%)")
    print(f"\nTotal Workload: {total_load:.1f} units | Mean Load per Worker: {avg_load:.1f} units")

def main():
    jobs = load_dataset(CSV_FILENAME)
    workers = ["Worker_A", "Worker_B", "Worker_C"]
    dynamic_load_balancing(jobs, workers)

if __name__ == "__main__":
    main()

# CSV FILE NAME: workload_308.csv
# CSV COLUMNS: job_id,compute_units,assigned_worker,status
# COLUMN MEANINGS:
# job_id: Unique identifier for each workload job
# compute_units: Computational units or load required to execute the job
# assigned_worker: Target worker node assignment (UNASSIGNED or designated worker)
# status: Current job status (PENDING/ASSIGNED/COMPLETED)
#
# SAMPLE CSV DATA:
# job_id,compute_units,assigned_worker,status
# J101,35,UNASSIGNED,PENDING
# J102,50,UNASSIGNED,PENDING
# J103,20,UNASSIGNED,PENDING
# J104,75,UNASSIGNED,PENDING
# J105,40,UNASSIGNED,PENDING
# J106,60,UNASSIGNED,PENDING
#
# SAVE AS: workload_308.csv
