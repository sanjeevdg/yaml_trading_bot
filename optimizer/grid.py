from itertools import product


class GridSearch:

    @staticmethod

    def build(grid):

        keys = grid.keys()

        values = grid.values()

        for combo in product(*values):

            yield dict(zip(keys, combo))
