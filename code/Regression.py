import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
from scipy import stats
from scipy.optimize import curve_fit
import sys
sys.path.append('../')
old_settings = np.seterr(all='ignore')


class Regression(object):
    '''
    This class will be used to fit the regression.
    '''
    def __init__(
            self,
            M1, # std 2 min mid-quote scaled to daily std
            M2, # volume
            M3, # arrival price, average of first five mid-quote prices
            M4, # imbalance between 9:30 and 3:30
            M5, # volume-weighted average price between 9:30 and 3:30
            M6, # volume-weighted average price between 9:30 and 4:00
            M7, # terminal price at 4:00 – Average of last five mid-quote price
    ):
        self.matrices = [M1, M2, M3, M4, M5, M6, M7]
        self.cleanMatrices(matrices=self.matrices)


    def residualHeteroskedasticityTest(self, alpha=0.05):
        xdata = self.xdata
        ydata = self.ydata
        popt, pcov = curve_fit(self.func, xdata, ydata)
        eta, beta = popt
        yhat = self.func(xdata, eta, beta)
        resid = ydata - yhat
        exog = [np.concatenate((([1.], ele))) for ele in xdata.T]
        # https://spu.fem.uniag.sk/cvicenia/ksov/obtulovic/Mana%C5%BE.%20%C5%A1tatistika%20a%20ekonometria/EconometricsGREENE.pdf
        # page 223
        # section 11.4.3
        bp_test = sm.stats.diagnostic.het_breuschpagan(resid, exog)
        t_stat = bp_test[0]
        pval = bp_test[1]
        print('-----------------------------------------------------')
        print('\nTest if the residuals are homoskedastic')
        print('The p value:', pval)
        if pval < alpha:  # null hypothesis: it is homoskedastic
            print("The null hypothesis can be rejected")
            print("Conclusion: the residuals are heteroskedastic")
        else:
            print("The null hypothesis cannot be rejected")
            print("Conclusion: the residuals are homoskedastic")
        self.residuHeteroPVal = pval

    def getResidualAnalysis(self):
        self.residualHeteroskedasticityTest()
        self.residualIndependenceTest()
        self.residualZeroMeanTest()
        self.residualNormalityTest()

    def residualZeroMeanTest(self, alpha=0.05):
        xdata = self.xdata
        ydata = self.ydata
        popt, pcov = curve_fit(self.func, xdata, ydata)
        eta, beta = popt
        yhat = self.func(xdata, eta, beta)
        resid = ydata - yhat
        residMean = np.mean(resid)
        residStd = np.std(resid)
        t_stat = residMean / residStd
        n = len(ydata)
        pval = stats.t.sf(np.abs(t_stat), n-1)
        self.residualZeroMeanTStat = t_stat
        self.residualZeroMeanPVal = pval
        print('-----------------------------------------------------')
        print('\nTest if the residuals have mean zero')
        print('The p value: ', pval)
        if pval < alpha:  # null hypothesis: mean is zero
            print("The null hypothesis can be rejected")
            print('The mean is not zero')
        else:
            print("The null hypothesis cannot be rejected")
            print('The mean is zero.')


    def residualIndependenceTest(self):
        xdata = self.xdata
        ydata = self.ydata
        popt, pcov = curve_fit(self.func, xdata, ydata)
        eta, beta = popt
        yhat = self.func(xdata, eta, beta)
        resid = ydata - yhat
        t_stat = durbin_watson(resid)
        self.residualIndependenceTStat = t_stat
        print('-----------------------------------------------------')
        print('\nTest if the residuals are independent')
        print('The t statistic:', t_stat)
        if t_stat < 1.5 or t_stat > 2.5:
            print('The residuals are not independent')
        else:
            print('The residuals are independent')


    def residualNormalityTest(self, alpha=0.05):
        # this if to find out if the residues are normally distributed
        xdata = self.xdata
        ydata = self.ydata
        popt, pcov = curve_fit(self.func, xdata, ydata)
        eta, beta = popt
        yhat = self.func(xdata, eta, beta)
        resid = self.ydata - yhat
        stat, pval = stats.normaltest(resid)
        print('-----------------------------------------------------')
        print('\nTest if the residuals are normally distributed')
        print('The p value:', pval)
        if pval < alpha:  # null hypothesis: x comes from a normal distribution
            print("The null hypothesis can be rejected")
            print('The residues does not follow a normal distribution.')
            print('This is a violation of the assumptions of non-linear regression')
        else:
            print("The null hypothesis cannot be rejected")
        fig = sm.qqplot(resid, line ='45')
        plt.show()
        plt.hist(resid, bins='auto')
        plt.xlim(-1, 1)
        plt.show()

        self.residNormalityPVal = pval


    def cleanMatrices(self, matrices, cutoff=10):
        # EXPE 173, MKC 306, MXM 323, NE 329, RTN 400
        # Only remove EXPE, MKC, MXM, NE, RTN tickers
        # They are at idx position [173, 306, 323, 329, 400]
        matrices = self.matrices
        def findFaulty(matrix):
            faultyList = []
            faultyDaysList = []
            totalDays = len(matrix[0])
            for i in range(len(matrix)):
                nonZeroCount = np.count_nonzero(matrix[i])
                zeroCount = totalDays - nonZeroCount
                if zeroCount > 0:
                    faultyList.append(i)
                    faultyDaysList.append(totalDays - nonZeroCount)
            return faultyList, faultyDaysList

        # cutoff is how many zeros are tolerable
        # for example, if cutoff is 30, then if a datapoint has 30 zeros in any input matrix
        # then the stock index corresponding to the datapoint will be documented to be purged later
        res = {}
        for idx, matrix in enumerate(matrices):
            d = {}
            d['idx'], d['zeros'] = findFaulty(matrix)
            matrixName = 'M' + str(idx + 1)
            res[matrixName] = d

        filteredIdxList = []
        filteredZeroList = []

        n = 7
        for ii in range(n):
            matrixName = 'M' + str(ii+1)
            matrixInfo = res[matrixName]
            idxList = matrixInfo['idx']
            zeroList = matrixInfo['zeros']
            for jj, ele in enumerate(zeroList):
                if ele > cutoff:
                    filteredIdxList.append(idxList[jj])
                    filteredZeroList.append(ele)

        self.faultyInfo = res
        faultyIdxList = sorted(list(set(filteredIdxList)))
        self.faultyIdxList = faultyIdxList

        cleanedMatrices = []

        for ele in matrices:
            cleanedMatrices.append(np.delete(ele, faultyIdxList, 0))

        self.cleanedMatrices = cleanedMatrices

        self.sigma, self.imbalance, self.value, self.h = self.prepareInputs(self.cleanedMatrices)
        self.xdata = np.array([self.imbalance.ravel(), self.value.ravel(), self.sigma.ravel()])
        self.ydata = self.h.ravel()

    def getSignificanceTestResults(self, count=100):
        # count is the number of bootstrapped eta and beta
        sigma, imbalance, value, h = self.sigma, self.imbalance, self.value, self.h 

        residualResult = self.sigTestResidual(sigma, imbalance, value, h, count=count)
        pairedResult = self.sigTestPaired(sigma, imbalance, value, h, count=count)
        return residualResult, pairedResult

    def getRegressionResults(self):
        sigma, imbalance, value, h = self.sigma, self.imbalance, self.value, self.h 
        eta, beta = self.calculateParameters(sigma, imbalance, value, h)
        return eta, beta

    def func(self, xdata, eta, beta):
        X = xdata[0]
        V = xdata[1]
        sigma = xdata[2]
        T = 6/6.5
        # calculate temporary impact 
        h = eta * sigma * np.sign(X) *  np.abs(X / (V * T)) ** beta
        return h

    def getComparisonIndices(self, targetMatrix):
        targetList = np.sum(targetMatrix, axis=1)
        self.targetList = targetList
        indexedTargetList = []
        idx = 0
        for target in targetList:
            indexedTargetList.append((idx, int(target)))
            idx += 1
        sortedTargetList = sorted(indexedTargetList, key = lambda x: x[1], reverse=True) # sorted descending order based on 2nd element
        sortedTargetIndices = [ele[0] for ele in sortedTargetList]
        middleIdx = len(sortedTargetIndices) // 2
        activeIndices = sortedTargetIndices[:middleIdx]
        inactiveIndices = sortedTargetIndices[middleIdx:]

        self.activeIndices = activeIndices
        self.inactiveIndices = inactiveIndices

        return activeIndices, inactiveIndices

    def getComparisonMatrices(self):
        # we assume the activity is reflected the the volume
        # targetMatrix is M2 * M6, which is the value = volume * VWAP930 to 400
        matrices = self.cleanedMatrices
        M2 = matrices[1]
        M6 = matrices[5]
        valueFull = M2 * M6
        activeIndices, inactiveIndices = self.getComparisonIndices(valueFull)

        activeMatrices = []
        inactiveMatrices = []
        for idx in range(len(matrices)):
            activeMatrices.append(matrices[idx][activeIndices])
            inactiveMatrices.append(matrices[idx][inactiveIndices])

        self.activeMatrices = activeMatrices
        self.inactiveMatrices = inactiveMatrices

        return activeMatrices, inactiveMatrices

    def getActivityAnalysis(self):
        activeMatrices, inactiveMatrices = self.getComparisonMatrices()
        
        activeSigma, activeImbalance, activeValue, activeH = self.prepareInputs(activeMatrices)
        activeEta, activeBeta = self.calculateParameters(activeSigma, activeImbalance, activeValue, activeH)

        inactiveSigma, inactiveImbalance, inactiveValue, inactiveH = self.prepareInputs(inactiveMatrices)
        inactiveEta, inactiveBeta = self.calculateParameters(inactiveSigma, inactiveImbalance, inactiveValue, inactiveH)

        activeResult = [activeEta, activeBeta]
        inactiveResult = [inactiveEta, inactiveBeta]

        self.activeSigma, self.activeImbalance, self.activeValue, self.activeH = activeSigma, activeImbalance, activeValue, activeH
        self.inactiveSigma, self.inactiveImbalance, self.inactiveValue, self.inactiveH = inactiveSigma, inactiveImbalance, inactiveValue, inactiveH

        return activeResult, inactiveResult


    # significance test with residual bootstrapping
    def sigTestResidual(self, sigma, imbalance, value, h, count=100):
        kk = count   # number of etas and betas that need to be bootstrapped
        # step 1.1
        xdata = self.xdata
        ydata = self.ydata
        popt, pcov = curve_fit(self.func, xdata, ydata)
        # step 1.2
        eta, beta = popt
        yhat = self.func(xdata, eta, beta)
        residues = self.ydata - yhat
        residuesLength = len(residues)

        bootstrappedEtaList = []
        bootstrappedBetaList = []

        np.random.seed(2022)
        # step 5
        while len(bootstrappedEtaList) < kk:
            try:
                # step 2 
                boot_resi = np.random.choice(residues,size=residuesLength,replace=True)
                # step 3
                y_boot = yhat + boot_resi
                # step 4
                popt, pcov = curve_fit(self.func, self.xdata, y_boot)
            except:
                continue
            bootstrappedEtaList.append(popt[0])
            bootstrappedBetaList.append(popt[1])
        assert(len(bootstrappedEtaList) == len(bootstrappedBetaList))
        assert(len(bootstrappedEtaList) == count)
        # degree of freedom
        df = len(ydata) - 2

        # step 6
        etaStd = np.std(bootstrappedEtaList, ddof=1)
        t_eta = eta/etaStd
        eta_pval = stats.t.sf(t_eta, df=df) * 2

        # step 6
        betaStd = np.std(bootstrappedBetaList, ddof=1)
        t_beta = beta/betaStd
        beta_pval = stats.t.sf(t_beta, df=df) * 2

        return t_eta, t_beta, eta_pval, beta_pval

    # significance test with paired bootstrapping
    def sigTestPaired(self, sigma, imbalance, value, h, count=100):
        kk = count   # number of etas and betas that need to be bootstrapped
        # step 1
        xdata = self.xdata
        ydata = self.ydata
        popt, pcov = curve_fit(self.func, xdata, ydata)
        eta = popt[0]
        beta = popt[1]

        np.random.seed(2022)
        n = len(xdata[0]) # length of xdata's sublist, xdata = [imbalance, value, sigma]
        
        bootstrappedEtaList = []
        bootstrappedBetaList = []
        # step 4
        while len(bootstrappedEtaList) < kk:
            try:
                # step 2
                idxList = np.random.choice(range(n),size = n, replace=True) # bootstrap the index list of data
                x_boot = np.array([imbalance.ravel()[idxList], value.ravel()[idxList], sigma.ravel()[idxList]])
                y_boot = ydata[idxList]
                # step 3
                popt, pcov = curve_fit(self.func, x_boot, y_boot)
            except:
                continue
            bootstrappedEtaList.append(popt[0])
            bootstrappedBetaList.append(popt[1])

        assert(len(bootstrappedEtaList) == len(bootstrappedBetaList))
        assert(len(bootstrappedEtaList) == count)
        # degree of freedom
        df = len(ydata) - 2

        # step 5
        etaStd = np.std(bootstrappedEtaList, ddof=1)
        t_eta = eta/etaStd
        eta_pval = stats.t.sf(t_eta, df=df) * 2

        # step 5
        betaStd = np.std(bootstrappedBetaList, ddof=1)
        t_beta = beta/betaStd
        beta_pval = stats.t.sf(t_beta, df=df) * 2

        return t_eta, t_beta, eta_pval, beta_pval

    # calculate eta and beta by performing regression
    def calculateParameters(self, sigma, imbalance, value, h):
        xdata = np.array([imbalance.ravel(), value.ravel(), sigma.ravel()])
        ydata = h.ravel()
        popt, pcov = curve_fit(self.func, xdata, ydata)
        eta = popt[0]
        beta = popt[1]
        return eta, beta


    # prepare inputs for temporary impact cost 
    def prepareInputs(self, matrices, lookBackNum=10, totalNum=65):
        M1 = matrices[0] # std 2 min mid-quote scaled to daily std
        M2 = matrices[1] # volume
        M3 = matrices[2] # arrival price, average of first five mid-quote prices
        M4 = matrices[3] # imbalance between 9:30 and 3:30
        M5 = matrices[4] # volume-weighted average price between 9:30 and 3:30
        M6 = matrices[5] # volume-weighted average price between 9:30 and 4:00
        M7 = matrices[6] # terminal price at 4:00 – Average of last five mid-quote price

        # the number of stocks
        rowCount = len(M1)
        # the number of 10 day look-backs
        colCount = len(M1[0]) - lookBackNum 
        
        startIdx = lookBackNum
        endIdx = totalNum

        # Prepare std of 2 min midquotes, std is scaled to daily.
        sigma = np.zeros((rowCount, colCount))
        ii = 0
        for col in range(startIdx, endIdx):
            # calculate the 10 day look-backs by averaging previous 10 days
            sigma[:, ii] = np.mean(M1[:,(col-startIdx):col], axis=1, keepdims=True).reshape((rowCount,))
            ii += 1
            
        # Prepare imbalance input
        # M5 VWAP 900 - 330
        # M4 original imbalance
        imbalanceFull = M4 * M5
        imbalance = imbalanceFull[:, 10:]
            
        # Prepare value input
        # value = daily volume * VWAP at 400
        valueFull = M2 * M6
        value = np.zeros((rowCount, colCount))
        ii = 0
        for col in range(startIdx, endIdx):
            # calculate the 10 day look-backs by averaging previous 10 days
            value[:, ii] = np.mean(valueFull[:,(col-startIdx):col], axis=1, keepdims=True).reshape((rowCount,))
            ii += 1
            
        # permImpact = g 
        #          g = 0.5 * ( s400 - s930 ) 
        #            = 0.5 * (terminal Price - arrival price) 
        #            = 0.5 * (M7 - M3)

        gFull = 0.5 * (M7 - M3) 

        # tempImpact = h
        #          h = ( s_tilda - s930 ) - g
        #            = ( s_tilda - arrival price ) - g
        #            = M5 - M3 - g

        # Prepare temporary impact
        hFull = M5 - M3 - gFull
        h = hFull[:, 10:]

        # return 10 day lookback matrices
        return sigma, imbalance, value, h