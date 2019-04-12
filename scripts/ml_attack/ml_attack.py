#!/usr/bin/python
import numpy as np
import scipy
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split

# from matplotlib.colors import ListedColormap
# import matplotlib.pyplot as plt

# def plot_decision_regions(X, y, classifier, test_idx=None, resolution=0.02):
#     # setup marker generator and color map
#     markers = ('s', 'x', 'o', '^', 'v')
#     colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
#     cmap = ListedColormap(colors[:len(np.unique(y))])
#
#     # plot the decision surface
#     x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
#     x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
#     xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
#                             np.arange(x2_min, x2_max, resolution))
#     Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
#     Z = Z.reshape(xx1.shape)
#     plt.contourf(xx1, xx2, Z, slpha=0.4, cmap=cmap)
#     plt.xlim(xx1.min(), xx1.max())
#     plt.ylim(xx2.min(), xx2.max())
#
#     # plot all samples
#     X_test, y_test = X[test_idx, :], y[test_idx]
#     for idx, cl in enumerate(np.unique(y)):
#         plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1],
#                     alpha=0.8, c=cmap(idx),
#                     marker=markers[idx], label=cl)
#
#     # highlight test samples
#     if test_idx:
#         X_test, y_test = X[test_idx, :], y[test_idx]
#         plt.scatter(X_test[:, 0], X_test[:, 1], c='',
#                     alpha=1.0, linewidth=1, marker='o',
#                     s=55, label='test set')

def main():

    # input bits are all ones
    # inbit = [1]*1024
    # print(inbit)
    inbit = []
    for i in range(1024):
        inbit.append([0, 1])

    # print(inbit)

    # weights are considered as 64 bit challenges to form 1024 CRPs
    w = []
    win = open("challenges.txt", "r")
    for line in win.readlines():
        w.append([])
        for i in line.split():
            w[-1].append(int(i))
    # print(w)
    # w = np.ndarray((2,), buffer=np.array(w), offset=np.int_().itemsize, dtype=int)
    # w_test = np.ndarray((2,), buffer=np.array([1, 2, 3]), offset=np.int_().itemsize, dtype=int)
    # print(w)

    result = []
    # output bits are single bit outputs in an array
    with open("output.txt", "r") as output_file:
        results = output_file.read().splitlines()
    # Convert to integer list
    results = list(map(int, results))
    # print(results)

    # training the classification model using scikit learn.linear_model LogisticRegression
    clf = linear_model.LogisticRegression(C=1000000)
    # print(results)
    # clf = linear_model.LogisticRegression(C=10000000.0, random_state=0)
    y=0.049

    w_train, w_test, results_train, results_test = train_test_split(w, results, test_size=y, random_state=0)
    y1=y*1024
    y1=int(y1)

    sc = StandardScaler()
    sc.fit(w_train)
    w_train_std = sc.transform(w_train)
    w_test_std = sc.transform(w_test)
    # w_train_std = w_train
    # w_test_std = w_test
    # print(w_train_std,w_test_std)

    w_combined_std = np.vstack((w_train_std, w_test_std))
    results_combined = np.hstack((results_train, results_test))
    # results_combined = results_train + results_test

    x = 0
    clf.fit(w_train_std, results_train)
    # print(clf.predict_proba(w_test_std))
    # for i in range(y1):
    #     if clf.predict(w_test_std[i])== results_test[i]:
    #         x+=1
    # pred_rate=(x/y1)*100
    arr = []
    arr = clf.predict(w_test_std)
    for i in range (len(arr)):
        if(arr[i] == results_test[i]):
            x+=1
    pred_rate=(x/len(arr))*100
    print(pred_rate)


    # clf.score(w_combined_std, results_combined)
    # results_combined = np.transpose(results_combined)
    # plot_decision_regions(w_combined_std, results_combined, classifier=clf, test_idx=range(105, 150))
    # plot_decision_regions(w_combined_std, results_combined, classifier=clf)



    # clf.fit(inbit, results, w)

    # # calculating the accuracy of the fit
    # clf.score(inbit, results, w)
    #
    # # predicting new output values based om previously used weights
    #
    # x = clf.predict(1, w[:, 67])
    # if x == results[0:67]:
    #     print("The prediction was correct\n")
    # else:
    #     print("\nnope sorry")


main()







