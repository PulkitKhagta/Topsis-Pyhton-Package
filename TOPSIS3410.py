import numpy as np
import pandas as pd
from scipy.stats import rankdata

def topsis(filepath, W, Z):
    data = pd.read_csv(filepath)
    X = data.iloc[:, 1:].values

    X = X.astype(float)
    m = len(X[0, :])

    for i in range(m):
        x = np.sqrt(np.sum(np.square(X[:, i])))
        X[:,i] = X[:, i]/x
    
    w = W/np.sum(W)

    for i in range(m):
        X[:,i] = X[:, i]*w[i]
    
    Aplus = np.zeros((m, 1), dtype = float)
    Aminus = np.zeros((m, 1), dtype = float)

    for i in range(m):
        if(Z[i] == '+'):
            Aplus[i] = np.max(X[:, i])
            Aminus[i] = np.min(X[:, i])
        if(Z[i] == '-'):
            Aplus[i] = np.min(X[:, i])
            Aminus[i] = np.max(X[:, i])

    Splus = np.zeros((len(X), 1), dtype = float)
    Sminus = np.zeros((len(X), 1), dtype = float)
        
    for j in range(m):
        Splus[:,0] += np.square(X[:, j] - Aplus[j])
        Sminus[:,0] += np.square(X[:, j] - Aminus[j])
    
    Splus[:] = np.sqrt(Splus[:])
    Sminus[:] = np.sqrt(Sminus[:])

    PerfM = np.zeros((len(X), 1), dtype = float)
    for i in range(len(X)):
        PerfM[i] = Sminus[i]/(Splus[i] + Sminus[i])
    
    rank = len(PerfM) - rankdata(PerfM, method = 'min').astype(int) + 1
    return rank