# Caution !!!

```
trades and quotes folder are omitted, but the FULL structure should be like the following.
```

# Instruction 

### Step 1
```
Put the relevant trades and quotes folder according to the following file structure.
```
### Step 2
```
Run UpdateMatricesRunner.ipynb to produce M1.txt, M2.txt, ... M7.txt
```
### Step 3
```
Relocate the M1.txt, M2.txt, ... M7.txt to matrices folder
Run UpdateMatricesRunner.ipynb to see the result.
(Since bootstrapping with large count is time-consuming, we have prepared RegressionRunnerResult.pdf for the final result)
```

### Tests
```
We put all the tests together in TestsRunner.ipynb, the output is in TestsRunner.pdf.
TestsRunner require the presence of trades and quotes folder.
```

# File Directory
### Collapsed Version
```
├─ code                                     
│  ├─ dbReaders (folder)                                           
│  ├─ impactModel (folder)                                              
│  ├─ Regression.py                         
│  ├─ RegressionRunner.ipynb                
│  ├─ RegressionRunnerResult.pdf            
│  ├─ ReturnBuckets.py                      
│  ├─ Test_FileManager.py                   
│  ├─ Test_FirstPriceBuckets.py             
│  ├─ Test_LastPriceBuckets.py              
│  ├─ Test_Regression.py                    
│  ├─ Test_ReturnBuckets.py                 
│  ├─ Test_TickTest.py                      
│  ├─ Test_UpdateMatrices.py                
│  ├─ Test_VWAP.py                          
│  ├─ TestsRunner.ipynb  (run all tests together)              
│  ├─ UpdateMatrices.py                     
│  ├─ UpdateMatricesRunner.ipynb            
│  ├─ validDays.txt                         
│  └─ validTickers.txt       
├─ trades                                                                      
├─ quotes                                        
├─ matrices                                                               
├─ README.md                                
├─ params_part1.txt                         
└─ report.pdf  
```

### Extended Version
```
algo_trading_hw2                            
├─ code                                     
│  ├─ dbReaders                             
│  │  ├─ FileNames.py                       
│  │  ├─ TAQQuotesReader.py                 
│  │  └─ TAQTradesReader.py                 
│  ├─ impactModel                           
│  │  ├─ FileManager.py                     
│  │  ├─ FirstPriceBuckets.py               
│  │  ├─ LastPriceBuckets.py                
│  │  ├─ TickTest.py                        
│  │  └─ VWAP.py                            
│  ├─ Regression.py                         
│  ├─ RegressionRunner.ipynb                
│  ├─ RegressionRunnerResult.pdf            
│  ├─ ReturnBuckets.py                      
│  ├─ Test_FileManager.py                   
│  ├─ Test_FirstPriceBuckets.py             
│  ├─ Test_LastPriceBuckets.py              
│  ├─ Test_Regression.py                    
│  ├─ Test_ReturnBuckets.py                 
│  ├─ Test_TickTest.py                      
│  ├─ Test_UpdateMatrices.py                
│  ├─ Test_VWAP.py                          
│  ├─ TestsRunner.ipynb                     
│  ├─ UpdateMatrices.py                     
│  ├─ UpdateMatricesRunner.ipynb            
│  ├─ validDays.txt                         
│  └─ validTickers.txt       
├─ trades                                                               
│  ├─ 20070620                         
│  │  ├─ A_trades.binRT
│  │  ├─ AA_trades.binRT
│  │  ├─ AAB_trades.binRT              
│  │  ├─ .......                        
│  │  ├─ ZXZZ_trades.binRT
│  │  └─ ZZ_trades.binRT                          
│  ├─ 20070920        
├─ quotes                                 
│  ├─ 20070620                               
│  ├─ ......                              
│  ├─ 20070920           
├─ matrices                                 
│  ├─ M1.txt                                
│  ├─ M2.txt                                
│  ├─ M3.txt                                
│  ├─ M4.txt                                
│  ├─ M5.txt                                
│  ├─ M6.txt                                
│  └─ M7.txt                                
├─ README.md                                
├─ params_part1.txt                         
└─ report.pdf                               
```