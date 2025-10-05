

from collections import deque
from typing import List, Tuple, Dict, Optional

def initial_state(n: int) -> str:
    """Return initial state for n rabbits on each side: 'E'*n + '_' + 'W'*n"""
    return 'E' * n + '_' + 'W' * n

def goal_state(n: int) -> str:
    """Return goal state for n rabbits on each side: 'W'*n + '_' + 'E'*n"""
    return 'W' * n + '_' + 'E' * n

def neighbors(state: str) -> List[Tuple[str, str]]:
    """
    Generate (next_state, move_description) pairs from a given state.
    Move description format: "<piece> from i -> j" (0-based indices)
    """
    res = []
    L = len(state)
    for i, ch in enumerate(state):
        if ch == 'E':
            # try step 1 to the right
            j = i + 1
            if j < L and state[j] == '_':
                new = list(state)
                new[i], new[j] = new[j], new[i]
                res.append((''.join(new), f"E {i} -> {j} (step)"))
            # try jump 2 to the right over one rabbit
            j2 = i + 2
            if j2 < L and state[j2] == '_' and state[i+1] in ('E', 'W'):
                new = list(state)
                new[i], new[j2] = new[j2], new[i]
                res.append((''.join(new), f"E {i} -> {j2} (jump)"))
        elif ch == 'W':
            # try step 1 to the left
            j = i - 1
            if j >= 0 and state[j] == '_':
                new = list(state)
                new[i], new[j] = new[j], new[i]
                res.append((''.join(new), f"W {i} -> {j} (step)"))
            # try jump 2 to the left over one rabbit
            j2 = i - 2
            if j2 >= 0 and state[j2] == '_' and state[i-1] in ('E', 'W'):
                new = list(state)
                new[i], new[j2] = new[j2], new[i]
                res.append((''.join(new), f"W {i} -> {j2} (jump)"))
    return res

def bfs_solve(start: str, goal: str) -> Optional[List[Tuple[str, str]]]:
    """
    BFS to find shortest path from start to goal.
    Returns list of (state, move_desc) from start (move_desc for first is '') to goal.
    """
    q = deque([start])
    parent: Dict[str, Optional[str]] = {start: None}
    move_desc: Dict[str, str] = {start: ""}

    while q:
        cur = q.popleft()
        if cur == goal:
            # reconstruct path
            path: List[Tuple[str, str]] = []
            s = cur
            while s is not None:
                path.append((s, move_desc[s]))
                s = parent[s]
            path.reverse()
            return path

        for nxt, md in neighbors(cur):
            if nxt not in parent:
                parent[nxt] = cur
                move_desc[nxt] = md
                q.append(nxt)
    return None

def pretty_print_solution(path: List[Tuple[str, str]]):
    """Print the solution path nicely"""
    if not path:
        print("No solution found.")
        return
    print(f"Total steps: {len(path)-1}\n")
    print(f"{'Step':>4}  {'State':<30}  Move")
    print("-" * 60)
    for step, (state, md) in enumerate(path):
        # display with spaces between characters for readability
        spaced = ' '.join(state)
        if step == 0:
            print(f"{step:>4}  {spaced:<30}  (start)")
        else:
            print(f"{step:>4}  {spaced:<30}  {md}")

def solve_and_print(n: int = 3):
    """Set up puzzle for n rabbits on each side and solve it"""
    start = initial_state(n)
    goal = goal_state(n)
    print(f"Solving rabbit-leap puzzle for n = {n}")
    print(f"Start: { ' '.join(start) }")
    print(f"Goal : { ' '.join(goal) }\n")
    path = bfs_solve(start, goal)
    if path is None:
        print("No solution found.")
    else:
        pretty_print_solution(path)

if __name__ == "__main__":
    # default n = 3 (three rabbits each side)
    solve_and_print(3)
