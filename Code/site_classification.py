
from sklearn import datasets
from sklearn.multiclass import OutputCodeClassifier
from sklearn.svm import SVC
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from sklearn.metrics.pairwise import euclidean_distances
import sklearn.metrics.pairwise as Kern
from sklearn import preprocessing 
import glob
import os
from sklearn.model_selection import KFold, cross_val_score
from sklearn.model_selection import GridSearchCV

def datasetLabels(NormalizationFlag,SimilarityFlag,filepath):
    dataset_list = []
    cwd = os.getcwd()
    for files in glob.glob(cwd +filepath+ "*.csv"):
        dataset_list.append(files)
    
    N = len(dataset_list)
    dataset = genfromtxt(dataset_list[1], delimiter=',')
    datasetTotal = np.zeros([1,dataset.shape[1]-1])
    print dataset.shape
    labelTotal = np.zeros([1])
    for site in range(0,N):
    
        dataset_file = dataset_list[site]
        dataset = genfromtxt(dataset_file, delimiter=',')
    
        if len(dataset.shape) == 2:
            datasetX = dataset[:,:-1]
            datasetID = dataset[:,-1]
        else: 
            dataset = dataset[np.newaxis,:]
            datasetX = dataset[:,:-1]
            datasetID = dataset[:,-1]
    
        if NormalizationFlag == 0:
            dataset_normalized = preprocessing.normalize(datasetX, norm='l2')
        elif NormalizationFlag == 1:
            dataset_normalized = preprocessing.scale(datasetX)
        elif NormalizationFlag == 2:
            min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
            dataset_normalized = min_max_scaler.fit_transform(datasetX)
        
        dataset_site = 'dataset' + str(site)
        exec (dataset_site + " = dataset_normalized")
        datasetTotal = np.concatenate((datasetTotal,dataset_normalized),axis = 0)
        labels = site*np.ones([dataset_normalized.shape[0]])
        labelTotal = np.concatenate((labelTotal,labels),axis = 0)
        
    datasetTotal = datasetTotal[1:,:]
    labelTotal = labelTotal[1:]
    
    return datasetTotal, labelTotal

filepath = "/Site_specific_data/"


NormalizationFlag = 1 # 0 is normalizing by norm, 1 is scale it, 2 is make it in between [0,1]
SimilarityFlag = 1 #0 if euclidean DISTANCE (note distance and similarity), 1 if RKHS (mean embedding) with linear kernel, 2 if RKHS with Gaussian kernel

<<<<<<< HEAD
X, Y = datasetLabels(NormalizationFlag,SimilarityFlag,filepath)
numInstances = X.shape[0]
numTrain = 500
ind = np.random.permutation(numInstances)
XTrain = X[ind[0:numTrain],:]
YTrain = Y[ind[0:numTrain]]
XTest = X[ind[numTrain:],:]
YTest = Y[ind[numTrain:]]

#print Y
clf = SVC()
clf.fit(XTrain, YTrain)
YPred = clf.predict(XTest)
print numTrain
print numInstances
print YPred.shape, YTest.shape
print np.sum(YPred == YTest)/float(numInstances - numTrain)

#plt.plot(YPred)
#plt.plot(Y)
#plt.show()
#print np.sum(YTest==0), np.sum(YTest==1),np.sum(YTest==2),np.sum(YTest==3),np.sum(YTest==4)
#print np.sum(YPred==0), np.sum(YPred==1),np.sum(YPred==2),np.sum(YPred==3),np.sum(YPred==4)
=======
T = 20
numTrain = 500
accu = np.zeros([T])
for tt in range(0,T):
    X, Y = datasetLabels(NormalizationFlag,SimilarityFlag,filepath)
    numInstances = X.shape[0]
    ind = np.random.permutation(numInstances)
    XTrain = X[ind[0:numTrain],:]
    YTrain = Y[ind[0:numTrain]]
    XTest = X[ind[numTrain:],:]
    YTest = Y[ind[numTrain:]]

    #print Y
    clf = SVC()
    clf.fit(XTrain, YTrain)
    YPred = clf.predict(XTest)
    print "size of test data"
    print YPred.shape, YTest.shape
    print "No Cross Validation Accuracy is"
    print np.sum(YPred == YTest)/float(numInstances - numTrain)

    #plt.plot(YPred)
    #plt.plot(Y)
    #plt.show()
    #print np.sum(YTest==0), np.sum(YTest==1),np.sum(YTest==2),np.sum(YTest==3),np.sum(YTest==4)
    #print np.sum(YPred==0), np.sum(YPred==1),np.sum(YPred==2),np.sum(YPred==3),np.sum(YPred==4)

    #k_fold = KFold(n_splits = 5)
    #[svc.fit(XTrain[train],yTrain[train]).score(XTrain[test],yTrain[test])for train,test in k_fold.split(XTrain)]

    CGrid = np.logspace(-4,1,20)
    GammaGrid = np.logspace(-3,3,20)
    clf_cv = GridSearchCV(estimator = SVC(kernel = 'rbf'), param_grid = dict(C = CGrid,gamma = GammaGrid),cv = 5)
    clf_cv.fit(XTrain,YTrain)
    print "Best parameters"
    print clf_cv.best_estimator_.C,clf_cv.best_estimator_.gamma

    clf = SVC(C = clf_cv.best_estimator_.C, gamma = clf_cv.best_estimator_.gamma,kernel = 'rbf')
    clf.fit(XTrain,YTrain)
    YPred = clf.predict(XTest)
    print "Size of test Data"
    print YPred.shape,YTest.shape,numInstances - numTrain
    print "Train Data Distribution according to classes are"
    TrainHist =  np.histogram(YTrain,20)[0]/float(numTrain)
    print TrainHist, np.sum(TrainHist)
    print "Test Data distribution according to classes are"
    TestHist =  np.histogram(YTest,20)[0]/float(numInstances-numTrain)
    print TestHist, np.sum(TestHist)
    print "Accuracy with Cross Validation is: "
    accu[tt] = np.sum(YPred == YTest)/float(numInstances - numTrain)
    print np.sum(YPred == YTest)/float(numInstances -numTrain)
>>>>>>> e00e7b6bd0be1037ecfb7fe281abd80955bdc7e0

print "Average accuracy is: " + str(np.mean(accu))
