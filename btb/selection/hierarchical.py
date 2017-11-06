from btb.selection import Selector, UCB1


class HierarchicalByAlgorithm(UCB1):
    def __init__(self, choices, **kwargs):
        """
        Needs:
            by_algorithm: {str -> list[choice]} grouping of frozen set choices
                by ML algorithm
        """
        super(HierarchicalByAlgorithm, self).__init__(choices, **kwargs)
        self.by_algorithm = kwargs.pop('by_algorithm')

    def select(self, choice_scores):
        """
        Groups the frozen sets by algorithm and first chooses an algorithm based
        on the traditional UCB1 criteria.

        Next, from that algorithm's frozen sets, makes the final set choice.
        """
        # choose algorithm using a bandit
        alg_scores = {}
        for algorithm, choices in self.by_algorithm.iteritems():
            # only make arms for algorithms that have options
            if not set(choices) & set(choice_scores.keys()):
                continue
            # sum up lists to get a list of all the scores from any run of this
            # algorithm
            alg_scores[algorithm] = sum(choice_scores.get(c, [])
                                        for c in choices)

        best_algorithm = self.bandit(alg_scores)

        # now use only the frozen sets from the chosen algorithm
        best_subset = self.by_algorithm[best_algorithm]
        normal_ucb1 = UCB1(choices=best_subset)
        return normal_ucb1.select(choice_scores)
