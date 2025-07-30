#pack is a module that takes an array and returns a rescaled array, input array times 2.
import numpy as np

def pack(arr: np.ndarray) -> np.ndarray:
    """
    Rescale the input array by a factor of 2.

    Args:
        arr (np.ndarray): Input array to be rescaled.

    Returns:
        np.ndarray: Rescaled array.
    """
    # Rescale the array by multiplying by 2
    return arr * 2
