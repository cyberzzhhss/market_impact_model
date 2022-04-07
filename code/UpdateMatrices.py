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

class UpdateMatrices(object):
    '''
    This class will be used to build return buckets, eg 2 minute returns
    '''

    def __init__(
            self,
            tickerIndex,
            dayIndex,
            M1,
            M2,
            M3,
            M4,
            M5,
            M6,
            M7

    ):
        self.M1 = M1
        self.M2 = M2
        self.M3 = M3
        self.M4 = M4
        self.M5 = M5
        self.M6 = M6
        self.M7 = M7
        with open('validDays.txt') as f1:
            validDays = [line.rstrip('\n') for line in f1]
        with open('validTickers.txt') as f2:
            validTickers = [line.rstrip('\n') for line in f2]
        baseDir = os.path.dirname(os.getcwd())
        fileName = "trades/"+str(validDays[dayIndex])+"/"+validTickers[tickerIndex]+"_trades.binRT" #ex. "trades/20070620/IBM_trades.binRT"
        #print(fileName)
        data = TAQTradesReader(baseDir + "/" + fileName)

        startTS930 = 18*60*60*1000/2
        endTS1530 = 31*60*60*1000/2
        endTS1600 = 16*60*60*1000
        
        
        #M1 average of 2min return
        returnBuckets = ReturnBuckets(data,startTS930,endTS1600,210)
        returnList = []
        for i in range(210):
            singleReturn = returnBuckets.getReturn(i)
            if singleReturn is not None:
                returnList.append(singleReturn)
        sigma = np.std(returnList) * np.sqrt(210)
        self.M1[tickerIndex][dayIndex]=sigma
        #Tests:
        """
        print(sigma)
        print(M1[tickerIndex][dayIndex])
        print(tickerIndex)
        print(dayIndex)
        print(M1[0][0])
        """
        
        #M5 VWAP from 930 to 1530
        vwap1530 = VWAP(data,startTS930,endTS1530)
        self.M5[tickerIndex][dayIndex]=vwap1530.getVWAP()

        #Test:
        #print(vwap1530.getVWAP())
        #print(M5[0][0])
        
        #M6 VWAP from 930 to 1600
        vwap1600 = VWAP(data,startTS930,endTS1600)
        self.M6[tickerIndex][dayIndex]=vwap1600.getVWAP()

        #Test:
        #print(vwap1600.getVWAP())
        #print(M6[0][0])
        
        #M2 total daily volume
        #M3 arrival price
        #M4 imbalance between 930 and 1530
        #M7 terminal price

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

        self.M2[tickerIndex][dayIndex]=tdv
        self.M3[tickerIndex][dayIndex]=ap/5
        self.M4[tickerIndex][dayIndex]=imb
        self.M7[tickerIndex][dayIndex]=tp/5
        #Tests:
        #print(classification[1][2])
        #print(M2[tickerIndex][dayIndex])
        #print(M3[tickerIndex][dayIndex])
        #print(M4[tickerIndex][dayIndex])
        #print(M7[tickerIndex][dayIndex])
    def getMatrices(self):
        return self.M1, self.M2, self.M3, self.M4, self.M5, self.M6, self.M7