#!/usr/bin/python
#coding = utf-8
import os

class pathObj():
    pathDict = {}
    pathDict['Any'] = 'Set' + os.sep + 'Security' + os.sep + 'base.py'
    pathDict['Stock'] = 'Set' + os.sep + 'Security' + os.sep + 'Stock' + os.sep + 'stock.py'
    pathDict[
        'Index Underlying Stock'] = 'Set' + os.sep + 'Security' + os.sep + 'Stock' + os.sep + 'stockIndexUnderlyingStock.py'
    pathDict['Fund'] = 'Set' + os.sep + 'Security' + os.sep + 'Fund' + os.sep + 'fund.py'
    pathDict['Bond'] = 'Set' + os.sep + 'Security' + os.sep + 'Bond' + os.sep + 'bond.py'
    pathDict[
        'Index Underlying Bond'] = 'Set' + os.sep + 'Security' + os.sep + 'Bond' + os.sep + 'bondIndexUnderlyingBond.py'
    pathDict['Derivative'] = 'Set' + os.sep + 'Security' + os.sep + 'Derivative' + os.sep + 'derivative.py'
    pathDict['Option'] = 'Set' + os.sep + 'Security' + os.sep + 'Derivative' + os.sep + 'Option' + os.sep + 'option.py'
    pathDict['Future'] = 'Set' + os.sep + 'Security' + os.sep + 'Derivative' + os.sep + 'Future' + os.sep + 'future.py'
    pathDict['Index Future'] = 'Set' + os.sep + 'Security' + os.sep + 'Derivative' + os.sep + 'Future' + os.sep + 'indexFuture.py'
    pathDict['Bond Future'] = 'Set' + os.sep + 'Security' + os.sep + 'Derivative' + os.sep + 'Future' + os.sep + 'bondFuture.py'
    pathDict['Repo'] = 'Set' + os.sep + 'Security' + os.sep + 'Repo' + os.sep + 'repo.py'
    pathDict['Convertible Bond'] = 'Set' + os.sep + 'Security' + os.sep + 'Bond' + os.sep + 'convertibleBond.py'
    pathDict['Interest Rate'] = 'Set' + os.sep + 'InterestRate' + os.sep + 'base.py'
    pathDict['Index'] = 'Set' + os.sep + 'Index' + os.sep + 'base.py'
    pathDict['Bond Index'] = 'Set' + os.sep + 'Index' + os.sep + 'BondIndex' + os.sep + 'bondIndex.py'
    pathDict['Stock Index'] = 'Set' + os.sep + 'Index' + os.sep + 'StockIndex' + os.sep + 'stockIndex.py'
    pathDict['Company'] = 'Set' + os.sep + 'Company' + os.sep + 'base.py'
    pathDict['Listed Company'] = 'Set' + os.sep + 'Company' + os.sep + 'ListedCompany' + os.sep + 'listedCompany.py'
    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<pathDictBegin>
    #-<pathDictEnd>

    listPathDict = {}
    listPathDict['Any'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'base.py'
    listPathDict['Stock'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'StockList' + os.sep + 'stockList.py'
    listPathDict[
        'Index Underlying Stock'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'StockList' + os.sep + 'stockIndexUnderlyingStockList.py'
    listPathDict['Fund'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'FundList' + os.sep + 'fundList.py'
    listPathDict['Bond'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'BondList' + os.sep + 'bondList.py'
    listPathDict[
        'Index Underlying Bond'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'BondList' + os.sep + 'bondIndexUnderlyingBondList.py'
    listPathDict['Derivative'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'DerivativeList' + os.sep + 'derivativeList.py'
    listPathDict['Option'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'DerivativeList' + os.sep + 'OptionList' + os.sep + 'optionList.py'
    listPathDict['Future'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'DerivativeList' + os.sep + 'FutureList' + os.sep + 'futureList.py'
    listPathDict['Index Future'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'DerivativeList' + os.sep + 'FutureList' + os.sep + 'indexFutureList.py'
    listPathDict['Bond Future'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'DerivativeList' + os.sep + 'FutureList' + os.sep + 'bondFutureList.py'
    listPathDict['Repo'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'RepoList' + os.sep + 'repoList.py'
    listPathDict['Convertible Bond'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'BondList' + os.sep + 'convertibleBondList.py'
    listPathDict['Index'] = 'Set' + os.sep + 'IndexList' + os.sep + 'base.py'
    listPathDict['Bond Index'] = 'Set' + os.sep + 'IndexList' + os.sep + 'BondIndexList' + os.sep + 'bondIndexList.py'
    listPathDict[
        'Stock Index'] = 'Set' + os.sep + 'IndexList' + os.sep + 'StockIndexList' + os.sep + 'stockIndexList.py'
    listPathDict['Company'] = 'Set' + os.sep + 'CompanyList' + os.sep + 'base.py'
    listPathDict[
        'Listed Company'] = 'Set' + os.sep + 'CompanyList' + os.sep + 'ListedCompanyList' + os.sep + 'listedCompanyList.py'
    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<listPathDictBegin>
    #-<listPathDictEnd>

    def __init__(self):
        pass




















