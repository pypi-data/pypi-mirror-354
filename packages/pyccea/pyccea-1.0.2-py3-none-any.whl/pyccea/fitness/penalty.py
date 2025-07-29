import numpy as np
from ..utils.datasets import DataLoader
from ..evaluation.wrapper import WrapperEvaluation
from ..fitness.function import WrapperFitnessFunction


class SubsetSizePenalty(WrapperFitnessFunction):
    """
    Objective function that penalizes large subsets of features.

    Rashid, A.N.M Bazlur, et al. "A novel penalty-based wrapper objective function for feature
    selection in Big Data using cooperative co-evolution." IEEE Access 8 (2020): 150113-150129.

    Attributes
    ----------
    w1: float
        Predictive performance weight.
    w2: float
        Penalty weight.
    """

    def __init__(self, evaluator: WrapperEvaluation, weights: list):
        super().__init__(evaluator)
        # Check the number of weights
        if len(weights) != 2:
            raise AssertionError(
                f"'{SubsetSizePenalty.__name__}' fitness function has only two components "
                "(predictive performance and penalty). Therefore, it requires only two weights."
            )
        # Check the sum of the weights
        if sum(weights) != 1:
            raise AssertionError(
                f"The sum of weights is {sum(weights)} but must be 1."
            )
        self.w1 = weights[0]
        self.w2 = weights[1]

    def evaluate(self, context_vector: np.ndarray, data: DataLoader):
        """
        Evaluate the given context vector using the fitness function.

        Parameters
        ----------
        context_vector: np.ndarray
            Solution of the complete problem.
        data: DataLoader
            Container with process data and training and test sets.

        Returns
        -------
        fitness: float
            Quality of the context vector.
        """
        penalty = context_vector.sum()/data.n_features
        evaluations = self._evaluate_predictive_performance(context_vector, data)
        evaluation = evaluations[self.evaluator.eval_function]
        # Since we are maximizing:
        # - For regression: invert the evaluation (lower error is better)
        # - For classification: use evaluation directly (higher accuracy is better)
        sign = -1 if self.evaluator.task == "regression" else 1
        fitness = sign * self.w1 * evaluation - self.w2 * penalty
        return fitness
