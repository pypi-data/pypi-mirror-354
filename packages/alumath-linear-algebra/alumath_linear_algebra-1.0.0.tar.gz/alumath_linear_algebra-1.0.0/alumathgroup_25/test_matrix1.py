#!/usr/bin/env python3

# Import the function and exception
mat_mul = __import__('main').multiply_matrices
MatrixDimensionError = __import__('main').MatrixDimensionError

# -----------------------------
# ✅ VALID TEST CASES
# -----------------------------

# Case 1: Basic valid 2x2 * 2x2
def test_valid_2x2():
    mat1 = [[1, 2],
            [3, 4]]
    mat2 = [[5, 6],
            [7, 8]]
    expected = [[19, 22],
                [43, 50]]
    try:
        result = mat_mul(mat1, mat2)
        assert result == expected, f"Expected {expected}, got {result}"
        print("✅ Test valid 2x2 passed")
    except Exception as e:
        print("❌ Test valid 2x2 failed:", e)

# Case 2: Rectangular valid 2x3 * 3x2
def test_rectangular():
    mat1 = [[1, 2, 3],
            [4, 5, 6]]
    mat2 = [[7, 8],
            [9, 10],
            [11, 12]]
    expected = [[58, 64],
                [139, 154]]
    try:
        result = mat_mul(mat1, mat2)
        assert result == expected, f"Expected {expected}, got {result}"
        print("✅ Test rectangular passed")
    except Exception as e:
        print("❌ Test rectangular failed:", e)

# Case 3: Single-element matrices
def test_single_element():
    mat1 = [[5]]
    mat2 = [[3]]
    expected = [[15]]
    try:
        result = mat_mul(mat1, mat2)
        assert result == expected, f"Expected {expected}, got {result}"
        print("✅ Test single-element passed")
    except Exception as e:
        print("❌ Test single-element failed:", e)


# -----------------------------
# ❌ INVALID TEST CASES (Should Raise Error)
# -----------------------------

# Case 4: Incompatible dimensions
def test_incompatible():
    mat1 = [[1, 2], [3, 4]]       # 2x2
    mat2 = [[5, 6, 7], [8, 9, 10]] # 2x3
    try:
        result = mat_mul(mat1, mat2)
        print("❌ Test incompatible failed: Expected error, but got result", result)
    except MatrixDimensionError as e:
        print("✅ Test incompatible passed:", e)
    except Exception as e:
        print("❌ Test incompatible failed: Wrong exception raised:", e)

# Case 5: Empty matrix
def test_empty_matrix():
    mat1 = []
    mat2 = [[1, 2], [3, 4]]
    try:
        result = mat_mul(mat1, mat2)
        print("❌ Test empty matrix failed: Expected error, but got result", result)
    except MatrixDimensionError as e:
        print("✅ Test empty matrix passed:", e)
    except Exception as e:
        print("❌ Test empty matrix failed: Wrong exception raised:", e)

# Case 6: Not a list (e.g., int instead of list)
def test_non_list_input():
    mat1 = 5
    mat2 = [[1, 2], [3, 4]]
    try:
        result = mat_mul(mat1, mat2)
        print("❌ Test non-list input failed: Expected error, but got result", result)
    except MatrixDimensionError as e:
        print("✅ Test non-list input passed:", e)
    except Exception as e:
        print("❌ Test non-list input failed: Wrong exception raised:", e)

# Case 7: Rows not all lists
def test_mixed_rows():
    mat1 = [[1, 2], "not a row", [3, 4]]
    mat2 = [[5, 6], [7, 8]]
    try:
        result = mat_mul(mat1, mat2)
        print("❌ Test mixed rows failed: Expected error, but got result", result)
    except MatrixDimensionError as e:
        print("✅ Test mixed rows passed:", e)
    except Exception as e:
        print("❌ Test mixed rows failed: Wrong exception raised:", e)

# Case 8: One matrix is empty row
def test_one_empty_row():
    mat1 = [[1, 2], [], [3, 4]]
    mat2 = [[5, 6], [7, 8]]
    try:
        result = mat_mul(mat1, mat2)
        print("❌ Test empty row failed: Expected error, but got result", result)
    except MatrixDimensionError as e:
        print("✅ Test empty row passed:", e)
    except Exception as e:
        print("❌ Test empty row failed: Wrong exception raised:", e)

# -----------------------------
# 🚀 Run All Tests
# -----------------------------

if __name__ == "__main__":
    print("🚀 Running test suite...\n")

    test_valid_2x2()
    test_rectangular()
    test_single_element()

    print()  # Separator
    test_incompatible()
    test_empty_matrix()
    test_non_list_input()
    test_mixed_rows()
    test_one_empty_row()

    print("\n🏁 Test suite completed.")