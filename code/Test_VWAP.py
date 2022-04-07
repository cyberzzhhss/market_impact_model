import unittest

from dbReaders import FileNames
from dbReaders.TAQTradesReader import TAQTradesReader
from impactModel.VWAP import VWAP
from dbReaders.FileNames import FileNames
import os

class Test_VWAP(unittest.TestCase):

    def testVWAP(self):
        filePathName = os.path.dirname(os.getcwd()) + "/trades/20070620/IBM_trades.binRT"
        start930 = 19 * 60 * 60 * 1000 / 2
        end4 = 16 * 60 * 60 * 1000
        vwap = VWAP(TAQTradesReader(filePathName), start930, end4)
        print("There were %d trades and a VWAP price of %f" % (vwap.getN(), vwap.getVWAP()))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testVWAP']
    unittest.main()
