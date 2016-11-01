import numpy as np
from matplotlib import pyplot as plt
from sklearn import neighbors
from sklearn.model_selection import KFold

def genDataSet(N):
    x = np.random.normal(0, 1, N)
    ytrue = (np.cos(x) + 2) / (np.cos(x * 1.4) + 2 )
    noise = np.random.normal(0, 0.2, N)
    y = ytrue + noise
    return x, y, ytrue

def main():
    X, y, ytrue = genDataSet(1000)
    plt.plot(X, y, '.')
    plt.plot(X, ytrue, 'rx')
    plt.savefig('hw4.problem1A.pdf', bbox_inches='tight')
    plt.show()

    X = X.reshape((len(X), 1))

    bestk = []
    kc = 0
    for n_neighbors in range(1, 900, 2):
        kf = KFold(10)
        kscore = []
        k = 0
        for train, test in kf.split(X):
            # print("%s %s" % (train, test))
            X_train, X_test, y_train, y_test = X[train], X[test], y[train], y[test]

            # time.sleep(100)

            # we create an instance of Neighbors Classifier and fit the data.
            clf = neighbors.KNeighborsRegressor(n_neighbors, weights='distance')
            clf.fit(X_train, y_train)

            kscore.append(abs(clf.score(X_test, y_test)))
            # print kscore[k]
            k = k + 1

        #print(n_neighbors)
        bestk.append(sum(kscore) / len(kscore))
        #print(bestk[kc])
        kc += 1

    # to do here: given this array of E_outs in CV, find the max, its
    # corresponding index, and its corresponding value of n_neighbors
    index = [0, 1, 2]
    topk = bestk[0:len(index)]
    for i in range(3, len(bestk)):
        if topk[0] < bestk[i]:
            if topk[0] > topk[1]:
                if topk[1] > topk[2]:
                    topk[2] = topk[1]
                    index[2] = index[1]
                topk[1] = topk[0]
                index[1] = index[0]
            elif topk[0] > topk[2]:
                topk[2] = topk[0]
                index[2] = index[0]
            topk[0] = bestk[i]
            index[0] = i
        elif topk[1] < bestk[i]:
            if topk[1] > topk[2]:
                topk[2] = topk[1]
                index[2] = index[1]
            topk[1] = bestk[i]
            index[1] = i
        elif topk[2] < bestk[i]:
            topk[2] = bestk[i]
            index[2] = i
    for i in range(0, len(index)):
        index[i] = 2 * index[i] + 1
    print(topk)
    print(index)
    if topk[0] < topk[1]:
        topk[0] = topk[1]
        index[0] = index[1]
    if topk[0] < topk[2]:
        index[0] = index[2]
    clf = neighbors.KNeighborsRegressor(index[2], weights='distance')
    clf.fit(X,y)
    print("Eout (R^2): " + str(clf.score(X,y)))
    print("Eout true (R^2): " + str(clf.score(X,ytrue)))

main()