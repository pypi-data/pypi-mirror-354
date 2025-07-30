# test_pure_python.py - NO external libraries
from alumathgroup13 import matrix_multiply

print("=== Pure Python Matrix Multiplication Tests ===")

# Test 1: Basic 2x2
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
result = matrix_multiply(A, B)
print(f"2x2 Test: {result == [[19, 22], [43, 50]]}")

# Test 2: Different dimensions
A = [[1, 2, 3]]
B = [[4], [5], [6]]
result = matrix_multiply(A, B)
print(f"1x3 × 3x1 Test: {result == [[32]]}")

# Test 3: Error handling
try:
    matrix_multiply([[1, 2]], [[3], [4], [5]])
    print("Error Test: FAILED - Should have raised error")
except ValueError:
    print("Error Test: PASSED")

print("All tests use pure Python only - no external libraries!")