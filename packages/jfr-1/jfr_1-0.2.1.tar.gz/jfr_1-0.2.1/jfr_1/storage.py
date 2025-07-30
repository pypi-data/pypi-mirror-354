import json
import os

STORAGE_PATH = os.path.join(os.path.dirname(__file__), "user_algorithms.json")

def load_user_algorithms():
    """Load algorithms from the user_algorithms.json file."""
    if not os.path.exists(STORAGE_PATH):
        return []
    
    with open(STORAGE_PATH, "r") as f:
        algorithms = json.load(f)
        
        # Check that each algorithm has the 'code' key, or 'source_code' for backwards compatibility
        for algo in algorithms:
            if 'code' not in algo and 'source_code' not in algo:
                raise ValueError(f"Algorithm '{algo.get('name', 'Unknown')}' is missing 'code' or 'source_code' key.")
        
        return algorithms

def save_user_algorithm(name, description, code):
    """Save a new user algorithm to the user_algorithms.json file."""
    algorithms = load_user_algorithms()
    
    # Avoid duplicating algorithms with the same name
    for algo in algorithms:
        if algo['name'] == name:
            raise ValueError(f"Algorithm with the name '{name}' already exists.")

    algorithms.append({
        "name": name,
        "description": description,
        "code": code
    })
    
    # Save the updated list of algorithms back to the JSON file
    with open(STORAGE_PATH, "w") as f:
        json.dump(algorithms, f, indent=4)



