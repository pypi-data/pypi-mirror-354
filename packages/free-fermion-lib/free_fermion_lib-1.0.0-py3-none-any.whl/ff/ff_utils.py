"""
Free Fermion Utilities Module

Common utility functions for the free fermion codebase.

Copyright 2025 James.D.Whitfield@dartmouth.edu
Licensed under MIT License.
"""

import numpy as np


def _print(obj, k=9):
    """Printing with small number suppression (using numpy printoptions)

    Args:
        obj: Any object to be printed
        k: The number of decimal places to print

    Returns:
        None
    """
    try:
        val = np.array(obj)

        # get current precision
        p = np.get_printoptions()["precision"]

        # change to request precision
        np.set_printoptions(precision=k)

        # check if input is completely real
        # If it is don't print complex part
        if np.allclose(val.imag, np.zeros_like(val)):
            val = val.real

        # do the printing
        print(val.round(k))

        # reset precision
        np.set_printoptions(precision=p)
        return
    finally:
        return print(obj)


def clean(obj, threshold=1e-6):
    """
    Clean small numerical values from arrays or matrices.

    Args:
        obj: NumPy array or matrix to clean
        threshold: Values below this threshold are set to zero

    Note: if threshold is an integer, it will be converted to 10^-threshold

    Returns:
        Cleaned array with small values set to zero
    """

    if threshold > 1:
        # assume that an integer number of decimal places has been requested
        threshold = 10 ** (-threshold)

    approx_obj = np.round(obj / threshold) * threshold
    if np.allclose(approx_obj, obj, threshold):
        obj = approx_obj

    if hasattr(obj, "real") and hasattr(obj, "imag"):
        # Handle complex arrays

        # clean the arrays
        real_part = np.where(np.abs(obj.real) < threshold, 0, obj.real)
        imag_part = np.where(np.abs(obj.imag) < threshold, 0, obj.imag)

        # reduce to scalars as needed
        if real_part.size == 1:
            real_part = real_part.item()

        if imag_part.size == 1:
            imag_part = imag_part.item()

        # cast to real if there is no imaginary part
        if np.allclose(imag_part, 0):
            # make it real
            return real_part
        else:
            # return the cleaned arrays
            return real_part + 1j * imag_part
    else:
        # Handle real arrays
        real_part = np.where(np.abs(obj) < threshold, 0, obj)

        # reduce to scalars
        if real_part.size == 1:
            real_part = real_part.item()

        return real_part


def formatted_output(obj, precision=6):
    """
    Format numerical output with specified precision.

    Args:
        obj: Object to format
        precision: Number of decimal places

    Returns:
        Formatted string representation
    """
    if isinstance(obj, (int, float, complex)):
        if isinstance(obj, complex):
            if abs(obj.imag) < 1e-10:
                return f"{obj.real:.{precision}f}"
            else:
                return f"{obj.real:.{precision}f} + {obj.imag:.{precision}f}j"
        else:
            return f"{obj:.{precision}f}"
    else:
        return str(obj)


def generate_random_bitstring(n, k):
    """Generates a random bit string of length n with Hamming weight k.

    Based on `np.random.choice`

    Args:
        n: The length of the bit string.
        k: The Hamming weight (number of 1s).

    Returns:
        A NumPy array representing the bit string, or None if k is invalid.
    """
    if k < 0 or k > n:
        return None  # Invalid Hamming weight

    bitstring = np.zeros(n, dtype=int)

    indices = np.random.choice(n, size=k, replace=False)
    bitstring[indices] = 1
    return bitstring


def kron_plus(a, b):
    """Computes the direct sum of two matrices

    Args:
        a: First matrix
        b: Second matrix

    Returns:
        Direct sum matrix [[a, 0], [0, b]]
    """
    Z01 = np.zeros((a.shape[0], b.shape[1]))
    return np.block([[a, Z01], [Z01.T, b]])
