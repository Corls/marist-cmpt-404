import numpy as np
import matplotlib.pyplot as plt

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

    def plot(self):
        max = np.ceil(self.n[len(self.n)-1]+1)
        plt.xlim(0.0, max)
        plt.ylim(0.0, max)
        for i in range(1, len(self.n)):
            plt.plot(self.n[i-1], self.n[i], 'r.')
        plt.show()


def main():
    s = SampleSizer(0.05, 0.05, 10)
    size = s.calculate()
    print('You need at least ' + str(np.ceil(size)) + ' samples.')
    s.plot()

main()
