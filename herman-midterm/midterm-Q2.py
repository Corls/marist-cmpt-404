import numpy as np

class SampleSizer:
    def __init__(self, e, sigma, dvc):
        # Random linearly separated data
        self.e = 8/(e**2)
        self.d = dvc
        self.s = 4/sigma
        self.n = [1]

    def formulate(self, N):
        return self.e * np.log(self.s * ((2*N)**self.d + 1))

    def calculate(self):
        it = 0
        N = self.formulate(self.n[it])
        while N > self.n[it]:
            it += 1
            self.n.append(N)
            N = self.formulate(N)
            # print(str(it) + ': ' + str(N) + ' >= ' + str(self.n[it]))
        return N


def main():
    s = SampleSizer(0.05, 0.05, 10)
    size = s.calculate()
    print('You need at least ' + str(np.ceil(size)) + ' samples.')

main()