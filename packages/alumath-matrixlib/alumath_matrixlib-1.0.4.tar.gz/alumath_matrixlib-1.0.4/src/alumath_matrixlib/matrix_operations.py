def matrix_multiply(a, b):
    """
    Matrix multiplication with personality!
    Returns either:
    - The product matrix (for valid inputs)
    - A creative error message (for invalid cases)
    """
    # ASCII art definitions
    LOCKOUT_ART = r"""
    (•_•)
    <)   )╯
     /    \ 
    \(•_•)
     (   (> 
     /    \ 
    (•_•)
    <)   )>
     ‾‾‾‾
    """
    
    # Helper function for matrix validation
    def is_valid_matrix(m):
        if not isinstance(m, list) or not all(isinstance(row, list) for row in m):
            return False
        return len(m) > 0 and all(len(row) == len(m[0]) for row in m)
    
    # --- Main Validation ---
    try:
        # Phase 1: Basic sanity checks
        if not is_valid_matrix(a) or not is_valid_matrix(b):
            print(f"🔒 {LOCKOUT_ART}")
            print("Matrix Police Alert! These don't look like proper matrices!")
            return None
        
        # Phase 2: Dimension compatibility
        a_cols = len(a[0])
        b_rows = len(b)
        if a_cols != b_rows:
            print(f"🚧 {LOCKOUT_ART}")
            print(f"Cannot multiply {len(a)}x{a_cols} and {b_rows}x{len(b[0])} matrices!")
            print("The columns of A must match rows of B")
            return None
        
        # Phase 3: Numerical validation
        if not all(isinstance(x, (int, float)) for row in a for x in row):
            print(f"🧮 {LOCKOUT_ART}")
            print("I only work with numbers, not hieroglyphics!")
            return None
        
        # --- Actual Calculation ---
        result = [
            [
                sum(a[i][k] * b[k][j] for k in range(len(b)))
                for j in range(len(b[0]))
            ]
            for i in range(len(a))
        ]
        
        # Success animation
        print("✅ Matrix multiplication successful!")
        print(r"""
         /\_/\
        ( o.o )
         > ^ <
        """)
        return result
        
    except Exception as e:
        # Catch-all for unexpected errors
        print(f"💥 {LOCKOUT_ART}")
        print("Critical System Failure! Just kidding...")
        print(f"But really: {type(e).__name__}: {str(e)}")
        print("Try matrices that can actually be multiplied!")
        return None