import unittest


def is_valid(s):
    x = 0
    for c in s:
        if c == ')':
            x -= 1
        elif c == '(':
            x += 1
        if x < 0:
            return False
    return x == 0


def min_cost_partition(s, weights):

    # dp[b][e] = min cost to make s[b:e+1] a valid string
    # dp[b][e] = min(ss = (dp[b][i - 1] + dp[i][e]) for i in range(b, e) if is_valid(ss), )
    dp = []
    for _ in range(len(s)):
        dp.append([0] * len(s))

    for i, w in enumerate(weights):
        dp[i][i] = 0 if s[i] == '_' else w

    for i in range(0, len(s) - 1):
        if s[i:i+2] == ')(':
            dp[i][i+1] = weights[i] + weights[i + 1]
        elif s[i:i+2] == '))':
            dp[i][i+1] = weights[i]
        elif s[i:i+2] == ')_':
            dp[i][i+1] = weights[i]
        elif s[i:i+2] == '((':
            dp[i][i+1] = weights[i + 1]
        elif s[i:i+2] == '(_':
            dp[i][i+1] = min(weights[i + 1], weights[i])
        elif s[i:i+2] == '()':
            dp[i][i+1] = 0
        elif s[i:i+2] == '__':
            dp[i][i+1] = 0

    for l in range(2, len(s)):
        for b in range(len(s) - l):
            e = b + l
            dp[b][e] = 0 if is_valid(s[b:e+1]) else float('inf')
            for i in range(b, e + 1):
                dp[b][e] = min(dp[b][i - 1] + dp[i][e], dp[b][e])

    return dp[0][len(s) - 1]



def min_cost(s, weights):
    return min_cost_partition(s, weights)




class MinCostTests(unittest.TestCase):

    def test_sample(self):
        s = "(_()_"
        w = [1, 5, 2, 3, 4]

        cost = min_cost(s, w)
        assert cost == 1, f"{cost} != 1"

    def test_adversarial(self):
        s = ")_()_"
        w = [5, 1, 2, 3, 4]

        cost = min_cost(s, w)
        assert cost == 5

    def test_long(self):
        s = "_" * 1000
        w = [5] * 1000

        cost = min_cost(s, w)
        assert cost == 0

    def test_several(self):
        tests = [
            (
                "))_",
                [5,1, 7],
                5
            ),
            (
                "))",
                [5,1],
                5
            ),
            (
                "))()((",
                [1, 2, 3, 4, 5, 6],
                7
            ),
            (
                ")",
                [7],
                7
            ),
            (
                "_",
                [7],
                0
            ),
        ]

        for s, w, expected in tests:
            cost = min_cost(s, w)
            assert cost == expected, f"{cost} != {expected}"


if __name__ == "__main__":
    with open('input.txt') as f:
        while True:
            s = next(f).strip()
            weights = [int(x) for x in next(f).strip().split()]

            cost = min_cost(s, weights)
