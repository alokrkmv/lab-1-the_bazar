# d = [
# [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
# [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
# [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
# [0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
# [0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
# [0, 0, 0 ,0 ,1, 0, 1, 1, 0, 0],
# [0, 0, 0 ,0 ,1, 1, 0, 1, 0, 0],
# [0, 0, 0 ,0, 0, 1, 1, 0, 1, 0],
# [0, 0, 0 ,0, 0, 0, 0, 1, 0, 1],
# [0, 0, 0 ,0, 0, 0, 0, 0, 1, 0],
# ]

# d = [
#     [0, 1, 0, 0, 0, 1],
#     [1, 0, 1, 0, 0, 0],
#     [0, 1, 0, 1, 1, 0],
#     [0, 0, 1, 0, 1, 0],
#     [0, 0, 1, 1, 0, 1],
#     [1, 0, 0, 0, 1, 0]
# ]

d = [
    [0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0],
]


def hopcount(d):
    N = len(d)
    NBITS = 1 << N

    m = [[-2 for j in range(NBITS)] for i in range(N)]
    p = [[-2 for j in range(NBITS)] for i in range(N)]

    def subsolve(b, visited):
        if (visited == (1 << b)):
            p[b][visited] = -1
            return 0

        if (m[b][visited] == -2):
            best = -1
            bestPred = -1
            for i in range(N):
                if (i != b and ((visited >> i) & 1) and d[i][b] != -1):
                    x = subsolve(i, visited & ~(1 << b))
                    if (x != -1):
                        x += d[i][b]
                        if (x > best):
                            best = x
                            bestPred = i  
            m[b][visited] = best
            p[b][visited] = bestPred
        return m[b][visited]


    def solve():
        best = -1
        for b in range(N):
            x = subsolve(b, (1 << N) - 1)
            if (x > best):
                best = x
        return best
    return solve()

print(hopcount(d))
