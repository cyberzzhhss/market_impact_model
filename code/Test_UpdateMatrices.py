import unittest
from UpdateMatrices import UpdateMatrices

from impactModel import FileManager

from impactModel.FirstPriceBuckets import FirstPriceBuckets
from impactModel.LastPriceBuckets import LastPriceBuckets
from impactModel.TickTest import TickTest
from impactModel.VWAP import VWAP

from dbReaders import FileNames
from dbReaders.TAQTradesReader import TAQTradesReader
from dbReaders.TAQQuotesReader import TAQQuotesReader

from ReturnBuckets import ReturnBuckets

import os

import numpy as np


# Version 1802181651 
class Test_UpdateMatrices(unittest.TestCase):

    def test(self):
        with open('validDays.txt') as f1:
            validDays = [line.rstrip('\n') for line in f1]
        with open('validTickers.txt') as f2:
            validTickers = [line.rstrip('\n') for line in f2]
        numOfDays = len(validDays)
        numOfTickers =len(validTickers)

        #for dayIndex in range(numOfDays):
        #    print(validDays[dayIndex])

        #for tickerIndex in range(numOfTickers):
        #    print(validTickers[tickerIndex])

        M1 = np.zeros((numOfTickers,numOfDays))
        M2 = np.zeros((numOfTickers,numOfDays))
        M3 = np.zeros((numOfTickers,numOfDays))
        M4 = np.zeros((numOfTickers,numOfDays))
        M5 = np.zeros((numOfTickers,numOfDays))
        M6 = np.zeros((numOfTickers,numOfDays))
        M7 = np.zeros((numOfTickers,numOfDays))
        tickerIndex=3
        dayIndex=0
        updateMatrices = UpdateMatrices(tickerIndex,dayIndex,M1,M2,M3,M4,M5,M6,M7)
        M1,M2,M3,M4,M5,M6,M7=updateMatrices.getMatrices()
        baseDir = os.path.dirname(os.getcwd())
        fileName = "trades/"+str(validDays[dayIndex])+"/"+validTickers[tickerIndex]+"_trades.binRT" #ex. "trades/20070620/IBM_trades.binRT"
        #print(fileName)
        data = TAQTradesReader(baseDir + "/" + fileName)

        startTS930 = 18*60*60*1000/2
        endTS1530 = 31*60*60*1000/2
        endTS1600 = 16*60*60*1000
        
        #test M1 
        returnBuckets = ReturnBuckets(data,startTS930,endTS1600,210)
        returnList = []
        for i in range(210):
            singleReturn = returnBuckets.getReturn(i)
            if singleReturn is not None:
                returnList.append(singleReturn)
        sigma = np.std(returnList) * np.sqrt(210)
        self.assertTrue(M1[tickerIndex][dayIndex]==0.009783358278463357)
        
        #test M5 
        vwap1530 = VWAP(data,startTS930,endTS1530)
        self.assertTrue(M5[tickerIndex][dayIndex]==50.10681073946698)

        
        #test M6 
        vwap1600 = VWAP(data,startTS930,endTS1600)
        self.assertTrue(M6[tickerIndex][dayIndex]==50.08767614952133)

        #test M2, M3, M4, M7 total daily volume
        ticktest = TickTest()
        classification = ticktest.classifyAll(data,startTS930,endTS1600)

        tdv = 0
        ap = 0
        imb = 0
        tp = 0

        nRec = data.getN()
        for i in range(nRec):
            size = data.getSize(i)
            direction=classification[i][2]
            tdv = tdv +size
            imb = imb +size*direction
            if i <= 4:
                ap=ap + data.getPrice(i)
            elif i >= nRec-5:
                tp = tp + data.getPrice(i)

        self.assertTrue(M2[tickerIndex][dayIndex]==957004)
        self.assertTrue(M3[tickerIndex][dayIndex]==50.27199935913086)
        self.assertTrue(M4[tickerIndex][dayIndex]==-162396)
        self.assertTrue(M7[tickerIndex][dayIndex]==49.86599960327148)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()