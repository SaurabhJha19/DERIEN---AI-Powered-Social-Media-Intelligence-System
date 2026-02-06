import math

def sigmoid(z: float) -> float:
    return 1 / (1 + math.exp(-z))


def normalize(value: float, mean: float, std: float) -> float:
    """
    Z-score normalization followed by sigmoid compression.
    Returns value in range [0, 1].
    """
    if value is None:
        return 0.0

    if std == 0:
        return 0.5  # neutral score if no variance

    z = (value - mean) / std
    return sigmoid(z)
