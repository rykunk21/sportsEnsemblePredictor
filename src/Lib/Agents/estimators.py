class Estimator:
    """
    Some quantities we only intend to estimate
    This is the agent version we can use to estimate a quanity 
    """
    pass


class FunctionEstimator(Estimator):
    """
    This is the agent version of a neural network
    """
    pass

class NoiseEstimator(Estimator):
    """
    Estimate the noise in a dataset
    """
    pass

class DataEstimator(Estimator):
    """
    Estimate how much data is needed to learn on a dataset
    """
    pass









