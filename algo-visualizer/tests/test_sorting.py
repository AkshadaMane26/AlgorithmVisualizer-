import pytest
from algorithms.sorting import generate_sort_steps
def test_bubble():
    arr=[5,3,1,4,2]
    steps, final, dry = generate_sort_steps(arr, 'bubble')
    assert final == sorted(arr)
def test_quick():
    arr=[8,2,7,3,9,1]
    steps, final, dry = generate_sort_steps(arr, 'quick')
    assert final == sorted(arr)
