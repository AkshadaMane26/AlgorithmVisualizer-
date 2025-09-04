from algorithms.searching import generate_search_steps
def test_linear_found():
    arr=[5,1,3,9]
    steps, idx = generate_search_steps(arr, 'linear', 3)
    assert idx==2
def test_binary():
    arr=[1,3,5,7,9]
    steps, idx = generate_search_steps(arr, 'binary', 7)
    assert idx==3
