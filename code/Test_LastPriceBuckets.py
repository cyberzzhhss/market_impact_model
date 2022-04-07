import unittest
from dbReaders.FileNames import FileNames
from impactModel.LastPriceBuckets import LastPriceBuckets
from dbReaders.TAQTradesReader import TAQTradesReader


class StubTAQTradesReader(TAQTradesReader):
    def __init__(self, filePathName):
        # super( filePathName )
        self._data = [
            [10 * 60 * 60 * 1000, 59.30],
            [15 * 60 * 60 * 1000, 63.00],
            [1 + 15 * 60 * 60 * 1000, 63.52]
        ]

    def getN(self):
        return len(self._data)

    def getTimestamp(self, iRec):
        return self._data[iRec][0]

    def getPrice(self, iRec):
        return self._data[iRec][1]


class Test_LastPriceBuckets(unittest.TestCase):

    def testConstructor(self):
        startTS = None
        endTS = None
        numBuckets = 2
        dataReader = StubTAQTradesReader(None)
        fpb = LastPriceBuckets(dataReader, numBuckets, startTS, endTS)
        self.assertTrue(fpb.getN() == 2)
        self.assertTrue(
            fpb.getTimestamp(0) == (10 * 60 * 60 * 1000) and fpb.getTimestamp(1) == (1 + 15 * 60 * 60 * 1000))
        self.assertAlmostEqual(fpb.getPrice(0), 59.30, delta=0.0001)
        self.assertAlmostEqual(fpb.getPrice(1), 63.52, delta=0.0001)

    '''
    def testConstructor(self):
        
        startTS = None
        endTS = None
        numBuckets = 2
        baseDir = '/Users/leonmaclin/Documents/sampleTAQ/'
        fileName = 'trades/20070620/IBM_trades.binRT'
        data = TAQTradesReader( baseDir + fileName )
        
        fpb = LastPriceBuckets( data, numBuckets, startTS, endTS )
        self.assertTrue( fpb.getN() == 2 )
        self.assertTrue( fpb.getTimestamp( 0 ) == 45896000 and fpb.getTimestamp( 1 ) == 57599000 )
        self.assertTrue( fpb.getPrice( 0 ) > ( 106.72000122070312 - 0.0001 ) and fpb.getPrice( 0 ) < ( 106.72000122070312 + 0.0001 ) )
        self.assertTrue( fpb.getPrice( 1 ) > ( 106.0 - 0.0001 ) and fpb.getPrice( 1 ) < ( 106.0 + 0.0001 ) )
        
        print ("Finished")
    '''


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
