# jfr_1/module.py

import inspect
from .storage import save_user_algorithm  # Only import what is defined

# Store algorithms in a list
algorithms = []

def register_algorithm(name, function, description):
    """Register a new algorithm and save it."""
    algorithms.append({
        'name': name,
        'function': function,
        'description': description
    })

    # Save source code using the available storage function
    try:
        source = inspect.getsource(function)
        save_user_algorithm(name, description, source)
    except Exception as e:
        print(f"[ERROR] Could not save {name}: {e}")

def list_algorithms():
    """List all registered algorithms."""
    return [algo['name'] for algo in algorithms]

def get_algorithm(name):
    """Retrieve an algorithm by name."""
    for algo in algorithms:
        if algo['name'] == name:
            return algo
    raise ValueError(f"Algorithm '{name}' not found.")

