import numpy as np
import pytest
from phenopack.pack import pack


def test_rescale():
    """Test that rescale works correctly for a simple case."""
    input_array = np.array([1, 2, 3, 4, 5])
    output_array = pack(input_array)
    expected_array = np.array([2, 4, 6, 8, 10])
    np.testing.assert_allclose(output_array, expected_array)


@pytest.mark.parametrize(
    "input_array, expected_array",
    [(np.array([1, 2, 3, 4, 5]), np.array([2, 4, 6, 8, 10])), (np.array([5, 4, 3, 2, 1]), np.array([10, 8, 6, 4, 2]))],
)
def test_rescale_parameterized(input_array, expected_array):
    """Test that rescale works correctly for multiple cases."""
    output_array = pack(input_array)
    np.testing.assert_allclose(output_array, expected_array)



# def test_rescale_invalid_params(input_array):
#     """
#     Test that rescale raises an error when passed invalid parameters.
#     """
#     rescale(input_array)