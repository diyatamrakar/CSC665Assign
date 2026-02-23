# ============================================================
# Solvers — Backtracking, BFS, and DFS
# Authors: S. El Alaoui and Gemini
# ============================================================

import math
from collections import deque
import time

# Ensure SearchProblem is available from your problem file
# from the3jugs import SearchProblem 

"""
Depth-first backtracking with simple 'explored' pruning.
Stores the best (lowest-cost) path of states encountered to any goal.
This is a recursive implementation. 

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored 
        
"""

class BacktrackingSearch:
    def __init__(self, problem):
        self.best_cost = math.inf
        self.best_path = None
        self.explored = set()
        self.problem = problem

    def recurse(self, state, path, cost: int):
        if self.problem.is_end(state):
            if cost < self.best_cost:
                self.best_cost = cost
                self.best_path = path[:]
            return

        for action in self.problem.actions(state):
            next_state = self.problem.succ(state, action)
            key = str(next_state)
            if key not in self.explored:
                self.explored.add(key)
                self.recurse(next_state, path + [next_state], cost + self.problem.cost(state, action))

    def solve(self):
        start = self.problem.start_state()
        self.explored.add(str(start))
        self.recurse(start, [], 0)
        return dict(
            best_cost=self.best_cost,
            best_path=[self.problem.start_state()] + (self.best_path or []),
            found=(self.best_path is not None),
            expanded=len(self.explored),
        )
        
"""
Depth-first backtracking with simple 'explored' pruning (iterative).
Stores the best (lowest-cost) path of states encountered to any goal.
This is an iterative implementation. 

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored

"""

class BacktrackingSearchIterative:
    def __init__(self, problem):
        self.best_cost = math.inf
        self.best_path = None
        self.explored = set()
        self.problem = problem

    def solve(self):
        start = self.problem.start_state()
        self.explored.add(str(start))
         # Stack holds tuples: (state, path_from_after_start, cost_so_far)
        stack = [(start, [], 0)]

        while stack:
            state, path, cost = stack.pop()
            if self.problem.is_end(state):
                if cost < self.best_cost:
                    self.best_cost = cost
                    self.best_path = path[:]
                continue

            for action in reversed(list(self.problem.actions(state))):
                next_state = self.problem.succ(state, action)
                key = str(next_state)
                if key not in self.explored:
                    self.explored.add(key)
                    stack.append((next_state, path + [next_state], cost + self.problem.cost(state, action)))

        return dict(
            best_cost=self.best_cost,
            best_path=[self.problem.start_state()] + (self.best_path or []),
            found=(self.best_path is not None),
            expanded=len(self.explored),
        )
"""
Add an iterative implementation of DFS.
BFS explores nodes level by leveland is guaranteed to find a goal at minimum depth (the fewest steps).

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored
"""

class BFSSearch:
    def __init__(self, problem):
        self.problem = problem

    def solve(self):
        start = self.problem.start_state()
        queue = deque([(start, [], 0)])
        explored = {str(start)}
        total_actions = 0
        max_depth = 0

        while queue:
            state, path, cost = queue.popleft()
            if cost > max_depth: max_depth = cost

            if self.problem.is_end(state):
                avg_b = total_actions / len(explored) if explored else 0
                return dict(
                    best_cost=cost, 
                    best_path=[start] + path, 
                    found=True, 
                    expanded=len(explored),
                    solution_depth=cost,      # d
                    max_depth=max_depth,      # D
                    avg_branching=avg_b       # b
                )

            actions = self.problem.actions(state)
            total_actions += len(actions)
            for action in actions:
                next_state = self.problem.succ(state, action)
                if str(next_state) not in explored:
                    explored.add(str(next_state))
                    queue.append((next_state, path + [next_state], cost + 1))
        return dict(best_cost=math.inf, found=False, expanded=len(explored))
    
"""
Add an iterative implementation of DFS.
DFS explores along a path as deep as possible before backtracking 
and returns the first solution found, which may not be the shortest.

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored
"""

class DFSSearch:
    def __init__(self, problem):
        self.problem = problem

    def solve(self):
        start = self.problem.start_state()
        stack = [(start, [], 0)]
        explored = {str(start)}
        total_actions = 0
        max_depth = 0

        while stack:
            state, path, cost = stack.pop()
            if cost > max_depth: max_depth = cost

            if self.problem.is_end(state):
                avg_b = total_actions / len(explored) if explored else 0
                return dict(
                    best_cost=cost, 
                    best_path=[start] + path, 
                    found=True, 
                    expanded=len(explored),
                    solution_depth=cost, 
                    max_depth=max_depth,
                    avg_branching=avg_b
                )

            actions = self.problem.actions(state)
            total_actions += len(actions)
            for action in reversed(list(actions)):
                next_state = self.problem.succ(state, action)
                if str(next_state) not in explored:
                    explored.add(str(next_state))
                    stack.append((next_state, path + [next_state], cost + 1))
        return dict(best_cost=math.inf, found=False, expanded=len(explored))


