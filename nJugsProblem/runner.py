# ============================================================
# Runner — read test cases then run all solvers
# Authors: S. El Alaoui and Gemini
# ============================================================

import math
import json
import time  # <--- Added for tracking execution time

from solvers import *
from the3jugs import * 

"""
Runs all four algorithms on a test case 
and returns the results as a dictionary.

    ** Modify ** it to track the:
        execution time
    for each algorithm and add it to their respective 
    dictionaries (bt_res, bti_res, bfs_res and dfs_res)
"""
def run_case(case):
    capacities = case["capacities"]
    goal = case["goal"]

    problem = NJugsProblem(capacities=capacities, goal=goal)

    # Dictionary to map algorithm names to their classes for clean timing
    algs = {
        "backtracking": BacktrackingSearch,
        "backtrackingIter": BacktrackingSearchIterative,
        "bfs": BFSSearch,
        "dfs": DFSSearch
    }

    results_data = {}

    for name, search_class in algs.items():
        # --- Start Timer ---
        start_time = time.time()
        
        try:
            if name == "backtracking":
                try:
                    solver = search_class(problem)
                    res = solver.solve()
                except RecursionError:
                    # Keep existing Part 1 crash handling
                    res = dict(best_cost=math.nan, best_path=[], found=False, expanded=0)
            else:
                solver = search_class(problem)
                res = solver.solve()
        except Exception as e:
            print(f"Error in {name}: {e}")
            res = dict(best_cost=math.nan, best_path=[], found=False, expanded=0)
            
        # --- Stop Timer & Store ---
        res["time"] = time.time() - start_time
        results_data[name] = res

    return {
        "name": case.get("name", ""),
        "capacities": capacities,
        "start": [0, 0, 0],
        "goal": goal,
        "backtracking": results_data["backtracking"],
        "backtrackingIter": results_data["backtrackingIter"],
        "bfs": results_data["bfs"],
        "dfs": results_data["dfs"],
    }

"""
Reads the results stored in ``res`` and prints them.

You MAY MODIFY it to also include:
    Execution time
    Branching factor (b)
    Maximum depth (D)
    Depth of shallowest solution (d)

Follow the same output formatting.
"""
def pretty_print_result(res, show_paths=False):
    print("=" * 95)
    print(f"Case: {res['name']}")
    print(f" Capacities: {res['capacities']}")
    print(f" Start:      {tuple(res['start'])}")
    print(f" Goal:       {tuple(res['goal'])}")

    for alg in ["backtracking", "backtrackingIter", "bfs", "dfs"]:
        r = res[alg]
        status = "FOUND" if r.get("found") else "NO SOLUTION"
        
        # --- Part 3 Metric Extraction ---
        exec_time = f"{r.get('time', 0):.5f}s"
        b = f"{r.get('avg_branching', 0):.2f}"
        d = r.get("solution_depth", "N/A")
        D = r.get("max_depth", "N/A")

        # Printed output including new metrics
        print(f"  [{alg.upper():<16}] {status:<10} | cost={r.get('best_cost'):<4} | time={exec_time} | b={b} | d={d} | D={D}")
        
        if show_paths and r.get("found") and r.get("best_path"):
            print(f"   Path length: {len(r['best_path'])-1}")
            print("   Path states:")
            for s in r["best_path"]:
                print(f"     {tuple(s)}")
"""
DO NOT MODIFY 

Reads test cases from the file: path 

Expected JSON structure:
[
  {"name":"case1","capacities":[...],"start":[...],"goal":[...]},
  ...
]

To add more test cases, edit ``test_cases.json`` and follow the correct formatting (valid JSON, no trailing commas).
"""
def read_cases_from_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    cleaned = []
    for idx, case in enumerate(data, start=1):
        name = case.get("name", f"case_{idx}")
        caps = list(case["capacities"])
        goal = list(case["goal"])
        cleaned.append(dict(name=name, capacities=caps, goal=goal))
    return cleaned

# create the table 
def print_terminal_graph(results):
    print("\n" + "="*30)
    print(" VISUALIZING SOLUTION DEPTH (d)")
    print("="*30)
    
    # Sort results by sum of capacities
    sorted_res = sorted(results, key=lambda x: sum(int(c) for c in x['capacities']))
    
    for res in sorted_res:
        total_sum = sum(int(c) for c in res['capacities'])
        d = res['bfs'].get('solution_depth', 0)
        
        # Create a bar of characters. 1 char = 1 step depth.
        bar = "#" * d
        print(f"Sum {total_sum:3}: {bar} ({d})")

def main():
    tc_file = "test_cases.json"
    cases = read_cases_from_json(tc_file)
    
    results = []
    for case in cases:
        res = run_case(case)
        results.append(res)
        pretty_print_result(res)

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("\nWrote detailed results to results.json")
    
    print("\n| Case | Sum | d (BFS) | D (DFS) | b (BFS) | Time |")
    print("|------|-----|---------|---------|---------|------|")
    for res in results:
        s = sum(int(c) for c in res['capacities'])
        d = res['bfs'].get('solution_depth', 0)
        D = res['dfs'].get('max_depth', 0)
        b = res['bfs'].get('avg_branching', 0)
        t = res['bfs'].get('time', 0)
        print(f"| {res['name']} | {s} | {d} | {D} | {b:.2f} | {t:.5f}s |")

if __name__ == "__main__":
    main()
