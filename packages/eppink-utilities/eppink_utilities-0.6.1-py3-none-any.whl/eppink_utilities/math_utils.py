import numpy as np

def safe_divide(numerator, denominator):
    """
    Safely divide two numbers (scalars, arrays, or combinations thereof),
    avoiding division by zero or invalid operations and propagating NaNs
    from numerator or denominator.

    Parameters:
    ----------
    numerator : float, int, array-like
        The numerator(s) in the division.
    denominator : float, int, array-like
        The denominator(s) in the division.

    Returns:
    -------
    result : float or np.ndarray
        The result of the division. Any division by zero or invalid result
        (e.g., inf, -inf, nan) is replaced with np.nan.
        Also, if numerator or denominator is NaN at any position, result is NaN there.

    Side Effects:
    -------------
    Prints an error message to the terminal if any division by zero occurs.
    """
    numerator = np.asarray(numerator, dtype=float)
    denominator = np.asarray(denominator, dtype=float)

    # Detect division by zero positions before division
    zero_div_mask = (denominator == 0)

    with np.errstate(divide='ignore', invalid='ignore'):
        result = np.true_divide(numerator, denominator)

    # Create a mask where numerator or denominator is nan
    nan_mask = np.isnan(numerator) | np.isnan(denominator)

    # Also replace inf, -inf, and nan in result with nan
    invalid_mask = ~np.isfinite(result)

    # Combine masks so that all invalid places are nan
    combined_mask = nan_mask | invalid_mask

    if np.any(zero_div_mask):
        print("Error: Division by zero encountered.")

    if np.isscalar(result):
        if combined_mask:
            return np.nan
        return result

    result[combined_mask] = np.nan

    return result

if __name__ == "__main__":
    print("Test division with zeros and NaNs:")
    print(safe_divide([1, 1, np.nan], [0, 1, 2]))  # expected: [nan, 1, nan]
    print(safe_divide(5, np.nan))                  # expected: nan
    print(safe_divide(np.nan, 3))                   # expected: nan
    print(safe_divide(1, 0))                        # expected: nan
