#!/usr/bin/env python3
"""
Comprehensive test for alumathpeer11 library
"""

def main():
    print("🧮 TESTING alumathpeer11 LIBRARY 🧮")
    print("=" * 40)
    
    try:
        from alumathpeer11 import Matrix, create_matrix, identity_matrix, zero_matrix
        print("✓ All imports successful")
        
        # Test 1: Basic 2x2 multiplication
        print("\n1. Testing 2x2 multiplication:")
        m1 = create_matrix([[1, 2], [3, 4]])
        m2 = create_matrix([[5, 6], [7, 8]])
        result = m1 * m2
        expected = [[19, 22], [43, 50]]
        
        print(f"   {m1.to_list()} * {m2.to_list()}")
        print(f"   = {result.to_list()}")
        
        if result.to_list() == expected:
            print("   ✓ PASSED")
        else:
            print(f"   ✗ FAILED (expected {expected})")
        
        # Test 2: Different dimensions
        print("\n2. Testing 2x3 * 3x2 multiplication:")
        m3 = create_matrix([[1, 2, 3], [4, 5, 6]])  # 2x3
        m4 = create_matrix([[7, 8], [9, 10], [11, 12]])  # 3x2
        result2 = m3 * m4  # 2x2
        expected2 = [[58, 64], [139, 154]]
        
        print(f"   2x3 * 3x2 = 2x2")
        print(f"   Result: {result2.to_list()}")
        
        if result2.to_list() == expected2:
            print("   ✓ PASSED")
        else:
            print(f"   ✗ FAILED (expected {expected2})")
        
        # Test 3: Identity matrix
        print("\n3. Testing identity matrix:")
        identity = identity_matrix(2)
        result3 = m1 * identity
        
        print(f"   Matrix * Identity = Matrix")
        print(f"   {m1.to_list()} * {identity.to_list()} = {result3.to_list()}")
        
        if result3.to_list() == m1.to_list():
            print("   ✓ PASSED")
        else:
            print("   ✗ FAILED")
        
        # Test 4: Matrix properties
        print("\n4. Testing matrix properties:")
        print(f"   Matrix dimensions: {m3.rows}x{m3.cols}")
        print(f"   Element at (0,1): {m3.get(0, 1)}")
        print(f"   Element at (1,2): {m3.get(1, 2)}")
        
        if m3.rows == 2 and m3.cols == 3 and m3.get(0, 1) == 2:
            print("   ✓ PASSED")
        else:
            print("   ✗ FAILED")
        
        # Test 5: Error handling
        print("\n5. Testing error handling:")
        try:
            bad_m1 = create_matrix([[1, 2]])  # 1x2
            bad_m2 = create_matrix([[3], [4], [5]])  # 3x1
            bad_result = bad_m1 * bad_m2  # Should fail
            print("   ✗ FAILED (should have raised error)")
        except ValueError:
            print("   ✓ PASSED (correctly caught dimension error)")
        
        print("\n" + "=" * 40)
        print("🎉 ALL TESTS COMPLETED! 🎉")
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
    except Exception as e:
        print(f"✗ Test failed with error: {e}")

if __name__ == "__main__":
    main()