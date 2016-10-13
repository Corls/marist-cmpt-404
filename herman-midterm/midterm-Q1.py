import numpy as np
import random
import os, subprocess
import matplotlib.pyplot as plt
import copy
from numpy import genfromtxt


class Pocket:
    def __init__(self):
        # Random linearly separated data
        self.X = self.generate_points()

    def generate_points(self):
        X, y = self.make_dataset()
        N = len(X)
        bX = []
        for k in range(0, N):
            bX.append((np.concatenate(([1], X[k, :])), y[k]))

        # this will calculate linear regression at this point
        X = np.concatenate((np.ones((N, 1)), X), axis=1)  # adds the 1 constant
        self.linRegW = np.linalg.pinv(X.T.dot(X)).dot(X.T).dot(y)  # lin reg
        print(self.linRegW)

        return bX

    def make_dataset(self):
        for i in range(0, 2):
            dataset = genfromtxt('features.csv', delimiter=' ')
            y = dataset[:, 0]
            X = dataset[:, 1:]
            #Do the thing for each thing both at 0 & 1
            y[y!=i] = -1
            y[y==i] = +1
            ##It's time to get Graphical
            #Plot those points
            c0 = plt.scatter(X[y == -1, 0], X[y == -1, 1], 20, color='r', marker='x')
            c1 = plt.scatter(X[y == 1, 0], X[y == 1, 1], 20, color='b', marker='o')
            #Revv up your Legends
            plt.legend((c0, c1), ('All Other Numbers -1', 'Number Zero +1'), loc='upper right', scatterpoints=1, fontsize=11)
            plt.xlabel(r'$x_1$')
            plt.ylabel(r'$x_2$')
            #Crank the Title
            plt.title(r'Intensity and Symmetry of Digits')
            #And Save!
            plt.savefig('midterm.plot' + str(i+1) + '.pdf', bbox_inches='tight')
            plt.show()
        return X, y

    def plot(self):
        plt.xlim(0.0, 0.7)
        plt.ylim(-8.0, 1.5)
        l = np.linspace(-1.5, 2.5)
        V = self.linRegW
        a, b = -V[1] / V[2], -V[0] / V[2]
        plt.plot(l, a * l + b, 'k-') # ToDo:::The black line is Linear Regression
        V = self.bestW  # for Pocket
        a, b = -V[1] / V[2], -V[0] / V[2]
        plt.plot(l, a * l + b, 'r-') # ToDo:::The red line is the Pocket
        cols = {1: 'r', -1: 'b'}
        for x, s in self.X:
            plt.plot(x[1], x[2], cols[s] + '.')

    def classification_error(self, vec, pts=None):
        # Error defined as fraction of misclassified points
        if not pts:
            pts = self.X
        M = len(pts)
        n_mispts = 0
        # myErr = 0
        for x, s in pts:
            # myErr += abs(s - int(np.sign(vec.T.dot(x))))
            if int(np.sign(vec.T.dot(x))) != s:
                n_mispts += 1
        error = n_mispts / float(M)
        # print error
        # print myErr
        return error

    def choose_miscl_point(self, vec):
        # Choose a random point among the misclassified
        pts = self.X
        mispts = []
        for x, s in pts:
            if int(np.sign(vec.T.dot(x))) != s:
                mispts.append((x, s))
        return mispts[random.randrange(0, len(mispts))]

    def pla(self, w):
        # Initialize the weigths to zeros
        self.bestW = copy.deepcopy(w)  # for Pocket
        self.plaError = []
        self.pocketError = []  # for Pocket
        X, N = self.X, len(self.X)
        it = 0
        print(N)
        # Iterate until all points are correctly classified
        self.plaError.append(self.classification_error(w))
        self.pocketError.append(self.plaError[it])  # for Pocket
        while self.plaError[it] != 0 & it < N:
            #For the sake of sanity, be in the know while it iterates.
            if it % 500 == 0:
                print(it)
            it += 1
            # Pick random misclassified point
            x, s = self.choose_miscl_point(w)
            # Update weights
            w += s * x

            self.plaError.append(self.classification_error(w))
            if self.pocketError[it - 1] > self.plaError[it]:  # for Pocket
                self.pocketError.append(self.plaError[it])
                self.bestW = copy.deepcopy(w)
            else:
                self.pocketError.append(self.pocketError[it - 1])
        self.plot()
        return it, self.linRegW


def main():
    w = np.zeros(3)
    for i in range(0, 2):
        p = Pocket()
        it, w = p.pla(w)
        print(it)
        part = 'midterm.problem1'
        if i==0:
            part += 'AB'
        else:
            part += 'C'
        part += '.pdf'
        plt.savefig(part, bbox_inches='tight')
        plt.show()

main()