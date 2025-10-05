import random

def create_k_sat_instance(num_vars, clause_length, num_clauses):
    # Create a list of variable names using uppercase letters
    variable_names = [chr(i + 65) for i in range(num_vars)]
    
    # Initialize the k-SAT problem representation
    problem_representation = "(("
    current_clause = []

    for i in range(num_clauses * clause_length):
        # Randomly select a variable
        selected_var = random.choice(variable_names)
        
        # Remove the selected variable to ensure uniqueness in the clause
        variable_names.remove(selected_var)
        current_clause.append(selected_var)

        # After every k variables, form a clause
        if (i + 1) % clause_length == 0:
            # Randomly decide to negate the clause's variables
            for var in current_clause:
                if random.random() < 0.5:
                    problem_representation += "~"
                problem_representation += var
            
            # Reset the current clause and manage formatting
            if i != (num_clauses * clause_length - 1):
                problem_representation += ") and ("
            current_clause = []
            variable_names.extend(current_clause)  # Reintroduce variables for future clauses
        else:
            # Continue building the clause
            if len(current_clause) > 1:  # Avoid adding 'or' for the first variable
                problem_representation += " or "

    problem_representation += "))"
    
    return problem_representation

# Generate and print multiple k-SAT problems
for idx in range(10):
    print(f"Problem {idx + 1}: {create_k_sat_instance(12, 3, 4)}")
