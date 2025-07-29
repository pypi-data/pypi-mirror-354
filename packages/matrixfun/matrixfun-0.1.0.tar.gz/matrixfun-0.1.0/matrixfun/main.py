from multiplier import Matrix, MatrixMultiplier, MatrixMultiplicationError, multiply_matrices, create_matrix

def test_valid_multiplication():
    A = create_matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    B = create_matrix([
        [7, 8, 9],
        [9, 10, 11],
        [11, 12, 13]
    ])

    result = multiply_matrices(A, B)
    print("✅ Valid multiplication result:")
    print(result)

def test_invalid_multiplication():
    A = create_matrix([
        [1, 2],
        [3, 4]
    ])

    B = create_matrix([
        [5, 6],
        [7, 8],
        [9, 10]
    ])

    try:
        multiply_matrices(A, B)
    except MatrixMultiplicationError as e:
        print("\n❌ Expected error for invalid multiplication:")
        print(e)

if __name__ == "__main__":
    test_valid_multiplication()
    test_invalid_multiplication()
