#!/usr/bin/python
# coding = utf-8
import numpy as np
import pandas as pd
from RiskQuantLib.Set.SecurityList.BondList.bondList import setBondList
from RiskQuantLib.Set.SecurityList.StockList.stockList import setStockList
class setShitBondList(setBondList,setStockList):
    def __nullFunction__(self):
        pass
    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>