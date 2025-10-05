from collections import deque

class RiverState:
    def __init__(self, num_cannibals, num_missionaries, boat_on_start_side, parent=None):
        self.num_cannibals = num_cannibals
        self.num_missionaries = num_missionaries
        self.boat_on_start_side = boat_on_start_side
        self.parent = parent

    def is_safe(self):
        if self.num_missionaries < 0 or self.num_cannibals < 0 or self.num_missionaries > 3 or self.num_cannibals > 3:
            return False
        if self.num_missionaries == 0 or self.num_missionaries == 3:
            return True
        return self.num_missionaries >= self.num_cannibals

    def __eq__(self, other):
        return (self.num_cannibals == other.num_cannibals and 
                self.num_missionaries == other.num_missionaries and 
                self.boat_on_start_side == other.boat_on_start_side)

    def __hash__(self):
        return hash((self.num_cannibals, self.num_missionaries, self.boat_on_start_side))

def breadth_first_search():
    start_state = RiverState(3, 3, True)
    end_state = RiverState(0, 0, False)
    state_queue = deque([start_state])
    explored_states = set()
    
    while state_queue:
        current_state = state_queue.popleft()
        if current_state == end_state:
            return reconstruct_path(current_state)
        explored_states.add(current_state)
        possible_states = generate_next_states(current_state)
        
        for new_state in possible_states:
            if new_state not in explored_states:
                state_queue.append(new_state)
    return None

def generate_next_states(state):
    possible_states = []
    
    if state.boat_on_start_side:
        if state.is_safe():
            possible_states.append(RiverState(state.num_cannibals - 2, state.num_missionaries, not state.boat_on_start_side, state))
            possible_states.append(RiverState(state.num_cannibals - 1, state.num_missionaries - 1, not state.boat_on_start_side, state))
            possible_states.append(RiverState(state.num_cannibals, state.num_missionaries - 2, not state.boat_on_start_side, state))
            possible_states.append(RiverState(state.num_cannibals - 1, state.num_missionaries, not state.boat_on_start_side, state))
            possible_states.append(RiverState(state.num_cannibals, state.num_missionaries - 1, not state.boat_on_start_side, state))
    else:
        if state.is_safe():
            possible_states.append(RiverState(state.num_cannibals + 2, state.num_missionaries, not state.boat_on_start_side, state))
            possible_states.append(RiverState(state.num_cannibals + 1, state.num_missionaries + 1, not state.boat_on_start_side, state))
            possible_states.append(RiverState(state.num_cannibals, state.num_missionaries + 2, not state.boat_on_start_side, state))
            possible_states.append(RiverState(state.num_cannibals + 1, state.num_missionaries, not state.boat_on_start_side, state))
            possible_states.append(RiverState(state.num_cannibals, state.num_missionaries + 1, not state.boat_on_start_side, state))
    
    return [s for s in possible_states if s.is_safe()]

def reconstruct_path(state):
    solution_path = []
    while state.parent is not None:
        solution_path.append((state.num_cannibals, state.num_missionaries, state.boat_on_start_side))
        state = state.parent
    solution_path.reverse()
    return solution_path

final_path = breadth_first_search()
if final_path is None:
    print("No solution found")
else:
    for step in final_path:
        print(step)
