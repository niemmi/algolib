from unittest import TestCase
from .context import Directed, Undirected, floyd

#     1
#   /   \
# 0       3-4
#   \   /
#     2

CASES = [
    {
        'class': Undirected,
        'edges': [
            [0, 1, 1],
            [0, 2, 2],
            [1, 3, 4],
            [2, 3, 5],
            [3, 4, 7]
        ],
        'expected': {
            0: {0: 0, 1: 1, 2: 2, 3: 5, 4: 12},
            1: {0: 1, 1: 0, 2: 3, 3: 4, 4: 11},
            2: {0: 2, 1: 3, 2: 0, 3: 5, 4: 12},
            3: {0: 5, 1: 4, 2: 5, 3: 0, 4: 7},
            4: {0: 12, 1: 11, 2: 12, 3: 7, 4: 0}
        }
    },
    {
        'class': Directed,
        'edges': [
            [0, 1, 1],
            [0, 2, 2],
            [1, 3, 4],
            [2, 3, 5],
            [3, 4, 7]
        ],
        'expected': {
            0: {0: 0, 1: 1, 2: 2, 3: 5, 4: 12},
            1: {0: float('inf'), 1: 0, 2: float('inf'), 3: 4, 4: 11},
            2: {0: float('inf'), 1: float('inf'), 2: 0, 3: 5, 4: 12},
            3: {0: float('inf'), 1: float('inf'), 2: float('inf'), 3: 0, 4: 7},
            4: {0: float('inf'), 1: float('inf'), 2: float('inf'), 3: float('inf'), 4: 0}
        }
    },
    {
        'class': Directed,
        'edges': [
            [0, 1, 1],
            [0, 2, 2],
            [1, 3, 4],
            [2, 3, 5],
            [3, 4, -1]
        ],
        'expected': {
            0: {0: 0, 1: 1, 2: 2, 3: 5, 4: 4},
            1: {0: float('inf'), 1: 0, 2: float('inf'), 3: 4, 4: 3},
            2: {0: float('inf'), 1: float('inf'), 2: 0, 3: 5, 4: 4},
            3: {0: float('inf'), 1: float('inf'), 2: float('inf'), 3: 0, 4: -1},
            4: {0: float('inf'), 1: float('inf'), 2: float('inf'), 3: float('inf'), 4: 0}
        }
    },
]

class TestFloyd(TestCase):
    def test_floyd(self):
        for case in CASES:
            graph = case['class']()
            for x, y, w in case['edges']:
                graph.insert_edge(x, y, weight=w)
            self.assertEqual(case['expected'], floyd(graph))
