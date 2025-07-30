# jfr_1

This is a simple Python library for testing PyPI publishing.

## Installation
```bash
pip install jfr_1


# jfr_1 Library

jfr_1 is a Python library for algorithms.

## How to Add a New Algorithm

1. Implement your algorithm as a Python function.
2. Use the `register_algorithm` function to add it to the library.
3. Add a description of what your algorithm does.
4. If you'd like to share it, submit a pull request.

## Example

```python
from jfr_1 import register_algorithm

def bubble_sort(arr):
    """Sort a list using bubble sort."""
    for i in range(len(arr)):
        for j in range(0, len(arr)-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Register the algorithm
register_algorithm('bubble_sort', bubble_sort, 'Bubble Sort: An algorithm that repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order.')
