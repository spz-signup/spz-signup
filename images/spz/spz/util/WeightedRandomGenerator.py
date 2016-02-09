# -*- coding: utf-8 -*-

"""Random generators and helper functions.
"""

import random
import bisect


class WeightedRandomGenerator(object):
    """
    Returns a random index with a weighted probability.
    Positive floating point weights; don't have to add up to 1 or 100 or anything in particular.

    Taken from http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python

    Example:
      w = WeightedRandomGenerator([.1, .1, .5, .1, .1])
      hist = defaultdict(int)

      for i in range(1000):
          hist[w()] += 1

      print(hist)
      defaultdict(<type 'int'>, {0: 115, 1: 106, 2: 554, 3: 108, 4: 117})
    """
    def __init__(self, weights):
        self.totals = []
        running_total = 0

        assert len(weights) > 0, "Weights required"
        assert all(w > 0 for w in weights), "Only positive weights allowed"

        for w in weights:
            running_total += w
            self.totals.append(running_total)

    def __next__(self):
        rnd = random.random() * self.totals[-1]
        return bisect.bisect_right(self.totals, rnd)

    def __call__(self):
        return next(self)
