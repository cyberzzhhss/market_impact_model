import unittest
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Version 1802181651 
class Test_Regression(unittest.TestCase):

    def test(self):
        def func(xdata, eta, beta):
            X = xdata[0]
            V = xdata[1]
            sigma = xdata[2]
            T = 6/6.5
            h = eta * sigma * np.sign(X) *  np.abs(X / (V * T)) ** beta
            return h
        imbalanceMean =  50
        valueMean =  100
        sigmaMean =  0.0148
        hMean =  0.00145

        np.random.seed(2022)

        imbalance = np.random.normal(imbalanceMean, abs(0.02 * imbalanceMean), 1000)
        value = np.random.normal(valueMean, abs(0.02 * valueMean), 1000)
        sigma = np.random.normal(sigmaMean, abs(0.02 * sigmaMean), 1000)
        h = np.random.normal(hMean, abs(0.305 * hMean), 1000)

        xdata = [imbalance, value, sigma]
        ydata = np.array(h)

        popt, pcov = curve_fit(func, xdata, ydata)
        eta = popt[0]
        beta = popt[1]
        h_hat = func(xdata, eta, beta)
        #difference = np.mean(h) - np.mean(h_hat)
        self.assertAlmostEqual(np.mean(h), np.mean(h_hat), delta=0.00001)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()