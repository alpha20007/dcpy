import csv
import os
import threading
import time

# Application Domain: Distributed Data Syncing in Disaster Drone Networks
# Multithreaded Worker Simulation with Mutex Locks

CSV_FILENAME = "tasks_113.csv"

shared_mutex = threading.Lock()
completed_task_registry = []

def worker_routine(task):
    task_id = task["task_id"]
    thread_name = task["thread_name"]
    burst_ms = task["burst_ms"]
    priority = task["priority"]

    print(f"[THREAD {thread_name}] Attempting to acquire lock for Task {task_id} (Priority: {priority})...")
    with shared_mutex:
        print(f"[LOCK ACQUIRED] Thread {thread_name} acquired lock for Task {task_id}")
        time.sleep(burst_ms / 10000.0)
        completed_task_registry.append({
            "task_id": task_id,
            "worker": thread_name,
            "burst_ms": burst_ms,
            "priority": priority,
            "status": "COMPLETED"
        })
        print(f"[TASK PROCESSED] Thread {thread_name} finished Task {task_id} (Burst: {burst_ms:.0f}ms)")
        print(f"[LOCK RELEASED] Thread {thread_name} released lock for Task {task_id}")

def load_dataset(filename):
    if os.path.exists(filename):
        tasks = []
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                tasks.append({
                    "task_id": row["task_id"].strip(),
                    "thread_name": row["thread_name"].strip(),
                    "burst_ms": float(row["burst_ms"].strip()),
                    "priority": row["priority"].strip(),
                    "status": row["status"].strip()
                })
        return tasks
    print(f"Dataset '{filename}' not found. Running with default sample data.\n")
    return [
        {"task_id": "T1", "thread_name": "Worker_1", "burst_ms": 50.0, "priority": "HIGH", "status": "PENDING"},
        {"task_id": "T2", "thread_name": "Worker_2", "burst_ms": 30.0, "priority": "MEDIUM", "status": "PENDING"},
        {"task_id": "T3", "thread_name": "Worker_1", "burst_ms": 40.0, "priority": "LOW", "status": "PENDING"},
        {"task_id": "T4", "thread_name": "Worker_3", "burst_ms": 60.0, "priority": "HIGH", "status": "PENDING"},
        {"task_id": "T5", "thread_name": "Worker_2", "burst_ms": 25.0, "priority": "MEDIUM", "status": "PENDING"},
        {"task_id": "T6", "thread_name": "Worker_3", "burst_ms": 35.0, "priority": "HIGH", "status": "PENDING"}
    ]

def main():
    tasks = load_dataset(CSV_FILENAME)
    threads = []

    print("Launching multithreaded worker tasks with Mutex synchronization:")
    for task in tasks:
        t = threading.Thread(target=worker_routine, args=(task,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nFinal Completed Task List:")
    for item in completed_task_registry:
        print(f"  Task ID: {item['task_id']} | Worker: {item['worker']} | Priority: {item['priority']} | Burst: {item['burst_ms']:.0f}ms | Status: {item['status']}")

if __name__ == "__main__":
    main()

# CSV FILE NAME: tasks_113.csv
# CSV COLUMNS: task_id,thread_name,burst_ms,priority,status
# COLUMN MEANINGS:
# task_id: Unique identifier for each processing task
# thread_name: Designator name of the worker thread
# burst_ms: Processing burst duration in milliseconds
# priority: Task execution priority (HIGH/MEDIUM/LOW)
# status: Task status (PENDING/COMPLETED)
#
# SAMPLE CSV DATA:
# task_id,thread_name,burst_ms,priority,status
# T1,Worker_1,50,HIGH,PENDING
# T2,Worker_2,30,MEDIUM,PENDING
# T3,Worker_1,40,LOW,PENDING
# T4,Worker_3,60,HIGH,PENDING
# T5,Worker_2,25,MEDIUM,PENDING
# T6,Worker_3,35,HIGH,PENDING
#
# SAVE AS: tasks_113.csv
