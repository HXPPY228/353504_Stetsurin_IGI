import numpy as np

class MatrixBase:
    """Base class for matrix operations."""
    _default_low = 0  # Static attribute for default range
    _default_high = 100

    def __init__(self, rows, cols):
        """Initialize matrix dimensions."""
        self.rows = rows
        self.cols = cols
        self.matrix = None

    @property
    def matrix(self):
        """Get the matrix."""
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        """Set the matrix."""
        self._matrix = value

    def __str__(self):
        """String representation of the matrix."""
        return str(self.matrix)

class MatrixRandomizerMixin:
    """Mixin for random matrix generation."""
    def randomize(self, low=None, high=None):
        """Generate a random matrix."""
        low = low if low is not None else MatrixBase._default_low
        high = high if high is not None else MatrixBase._default_high
        return np.random.randint(low, high, size=(self.rows, self.cols))

class MatrixOperations(MatrixBase, MatrixRandomizerMixin):
    """Class for matrix operations with NumPy."""
    def __init__(self, rows, cols):
        """Initialize with dimensions and create a random matrix."""
        super().__init__(rows, cols)
        self.matrix = self.randomize()

    def swap_max_elements(self):
        """Swap maximum elements in the first and last columns."""
        idx_max_first = np.argmax(self.matrix[:, 0])  # Index of max in first column
        idx_max_last = np.argmax(self.matrix[:, -1])  # Index of max in last column
        self.matrix[idx_max_first, 0], self.matrix[idx_max_last, -1] = \
            self.matrix[idx_max_last, -1], self.matrix[idx_max_first, 0]