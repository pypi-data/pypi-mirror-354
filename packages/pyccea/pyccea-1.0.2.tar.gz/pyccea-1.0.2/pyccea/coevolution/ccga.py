import numpy as np
from ..coevolution.ccea import CCEA
from ..fitness.penalty import SubsetSizePenalty
from ..evaluation.wrapper import WrapperEvaluation
from ..cooperation.best import SingleBestCollaboration
from ..cooperation.random import SingleRandomCollaboration
from ..initialization.binary import RandomBinaryInitialization
from ..optimizers.genetic_algorithm import BinaryGeneticAlgorithm


class CCGA(CCEA):
    """Cooperative Co-Evolutionary Genetic Algorithm.

    Attributes
    ----------
    subcomp_sizes : list
        Number of features in each subcomponent.
    feature_idxs : np.ndarray
        Shuffled list of feature indexes.
    """

    def _init_collaborator(self):
        """Instantiate collaboration method."""
        self.best_collaborator = SingleBestCollaboration()
        self.random_collaborator = SingleRandomCollaboration(seed=self.seed)

    def _init_evaluator(self):
        """Instantiate evaluation method."""
        evaluator = WrapperEvaluation(
            task=self.conf["wrapper"]["task"],
            model_type=self.conf["wrapper"]["model_type"],
            eval_function=self.conf["evaluation"]["eval_function"],
            eval_mode=self.eval_mode,
            n_classes=getattr(self.data, "n_classes", None)
        )
        self.fitness_function = SubsetSizePenalty(
            evaluator=evaluator,
            weights=self.conf["evaluation"]["weights"]
        )

    def _init_subpop_initializer(self):
        """Instantiate subpopulation initialization method."""
        self.initializer = RandomBinaryInitialization(
            data=self.data,
            subcomp_sizes=self.subcomp_sizes,
            subpop_sizes=self.subpop_sizes,
            collaborator=self.random_collaborator,
            fitness_function=self.fitness_function
        )

    def _init_optimizers(self):
        """Instantiate evolutionary algorithms to evolve each subpopulation."""
        self.optimizers = list()
        # Instantiate an optimizer for each subcomponent
        for i in range(self.n_subcomps):
            optimizer = BinaryGeneticAlgorithm(
                subpop_size=self.subpop_sizes[i],
                n_features=self.subcomp_sizes[i],
                conf=self.conf
            )
            self.optimizers.append(optimizer)
