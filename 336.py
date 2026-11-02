import csv
import os
from concurrent.futures import ThreadPoolExecutor

# Application Domain: Distributed File Storage System (DFS)
# Simulated MPI Scatter-Gather Parallel Matrix Multiplication

CSV_FILENAME = "matrix_336.csv"

MULTIPLIER_MATRIX_B = [
    [1, 2, 0, 1],
    [0, 1, 3, 2],
    [2, 0, 1, 1],
    [1, 3, 2, 0]
]

def worker_dot_product(task_args):
    row_id, row_vals, matrix_b = task_args
    num_cols_b = len(matrix_b[0])
    result_row = []
    for col_idx in range(num_cols_b):
        dot_product = sum(row_vals[k] * matrix_b[k][col_idx] for k in range(len(row_vals)))
        result_row.append(dot_product)
    print(f"  [WORKER TASK] Processed {row_id} -> Computed Partial Dot Product: {result_row}")
    return row_id, result_row

def load_dataset(filename):
    if os.path.exists(filename):
        matrix_a = []
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                row_vals = [
                    int(row["col_0"].strip()),
                    int(row["col_1"].strip()),
                    int(row["col_2"].strip()),
                    int(row["col_3"].strip())
                ]
                matrix_a.append((row["row_id"].strip(), row_vals))
        return matrix_a
    print(f"Dataset '{filename}' not found. Running with default sample data.\n")
    return [
        ("R0", [2, 4, 1, 5]),
        ("R1", [3, 1, 0, 2]),
        ("R2", [1, 2, 3, 4]),
        ("R3", [5, 0, 2, 1]),
        ("R4", [2, 3, 1, 0]),
        ("R5", [4, 1, 2, 3])
    ]

def main():
    matrix_a = load_dataset(CSV_FILENAME)

    print("Master scattering matrix rows to worker tasks:")
    scatter_tasks = []
    for task_idx, (row_id, row_vals) in enumerate(matrix_a):
        print(f"  [MASTER SCATTER] Scattering {row_id} = {row_vals} to Worker Task {task_idx}")
        scatter_tasks.append((row_id, row_vals, MULTIPLIER_MATRIX_B))

    print("\nWorkers computing partial row dot products concurrently:")
    gathered_results = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        for res in executor.map(worker_dot_product, scatter_tasks):
            gathered_results.append(res)

    print("\nMaster gathering partial results into final product matrix C (A x B):")
    for row_id, result_row in gathered_results:
        print(f"  [MASTER GATHER] {row_id}: {result_row}")

if __name__ == "__main__":
    main()

# CSV FILE NAME: matrix_336.csv
# CSV COLUMNS: row_id,col_0,col_1,col_2,col_3
# COLUMN MEANINGS:
# row_id: Row identifier string (e.g. R0, R1)
# col_0: Integer value of column index 0
# col_1: Integer value of column index 1
# col_2: Integer value of column index 2
# col_3: Integer value of column index 3
#
# SAMPLE CSV DATA:
# row_id,col_0,col_1,col_2,col_3
# R0,2,4,1,5
# R1,3,1,0,2
# R2,1,2,3,4
# R3,5,0,2,1
# R4,2,3,1,0
# R5,4,1,2,3
#
# SAVE AS: matrix_336.csv
