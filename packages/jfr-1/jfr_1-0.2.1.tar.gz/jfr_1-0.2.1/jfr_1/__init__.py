# jfr_1/__init__.py
from .module import register_algorithm, list_algorithms, get_algorithm
from .storage import load_user_algorithms  # Importing from storage

# Load algorithms from JSON at import
def _load_user_algorithms():
    data = load_user_algorithms()  # Use the correct function from storage
    for algo in data:
        local_vars = {}
        try:
            exec(algo['source_code'], {}, local_vars)
            func = next(iter(local_vars.values()))
            register_algorithm(algo['name'], func, algo['description'])
        except Exception as e:
            print(f"[ERROR] Failed to load '{algo['name']}': {e}")

_load_user_algorithms()

__all__ = [
    "register_algorithm",
    "list_algorithms",
    "get_algorithm"
]
