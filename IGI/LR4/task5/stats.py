import numpy as np

class Statistics:
    """Class for statistical computations on matrices."""
    def __init__(self, matrix):
        """Initialize with a matrix."""
        self.matrix = matrix

    def mean(self):
        """Calculate the mean of the matrix."""
        return np.mean(self.matrix)

    def median(self):
        """Calculate the median of the matrix."""
        return np.median(self.matrix)

    def variance(self):
        """Calculate the variance of the matrix."""
        return np.var(self.matrix)

    def std_dev(self):
        """Calculate the standard deviation of the matrix."""
        return np.std(self.matrix)

    def correlation(self, col1, col2):
        """Calculate correlation between two columns."""
        return round(np.corrcoef(self.matrix[:, col1], self.matrix[:, col2])[0, 1], 2)