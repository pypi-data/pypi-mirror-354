#!/usr/bin/python
#coding = utf-8

import sys,os
import time
from RiskQuantLib.module import *
import numpy as np
import pandas as pd

path = sys.path[0] if not getattr(sys, 'frozen', False) else os.path.dirname(sys.executable)
# from RiskQuantLib.Build.build import buildAttr,buildInstrument
# buildInstrument(path+os.sep+'instrument.xlsx')
# buildAttr(path+os.sep+'test.xlsx')
# from RiskQuantLib.SecurityList.BondList.PandaBondList.pandaBondList import pandaBondList
# a = pandaBondList()
# a.addPandaBond('01','SHit')
# a.addPandaBond('02','BigSHit')
# a.addPandaBond('03','SmallSHit')
# a.addPandaBondSeries(['04','05','06'],['warmShit','coldshit','anothershit'])
# b = pandaBondList()
# b.addPandaBondSeries(['04','05','06'],['warmShit','coldshit','anothershit'])
# c = a+b
# b.setThisVarable(['04','05','06'],[1,50,129])
# d = c.groupBy('code')
# b.setThisVarable(['04','05','06'],[1,4,129])
# b.setIssuer(['04','05','06'],['A','B','V'])
# from RiskQuantLib.CompanyList.ListedCompanyList.listedCompanyList import listedCompanyList
# cl = listedCompanyList()
# cl.addCompanyFromSecurityList(c)
# b.setIssuer(['04','05','06'],['C','D','V'])
# from RiskQuantLib.Module import *
# a = mathTool.isnan(2)
# b = strTool.getDigitsFromStr('81290ndoas12901n')
# clearAttr()
# clearInstrumentPath()
# buildInstrument(path+os.sep+'instrument.xlsx')
# clearInstrumentPath()
# a = samuraiBondList()
# time0 = time.time()
# a.addSamuraiBondSeries([str(i) for i in range(5000)],[str(int(i/10))+'name' for i in range(5000)])
# a.setHoldingAmount([str(i) for i in range(5000)],[i for i in range(5000)])
# time1 = time.time()
# b = a.rolling(50).execFunc('sum','holdingAmount')
#
# a.setHoldingAmount([str(i) for i in range(5000)],[i*2 for i in range(5000)])
# a.execFunc('calMaxHoldingAmount')
# print(time1-time0,time.time()-time1,a)
# a = securityList()
# a.addSecuritySeries(['a_'+str(int(i/5)) for i in range(1001)],['name_'+str(int(i)) for i in range(1001)])
# k = securityList()
# k.addSecuritySeries(['k_'+str(int(i/6)) for i in range(2001)],['name_'+str(int(i)) for i in range(2001)])
# [setattr(i,'price',j) for i,j in zip(a, range(len(a)))]
# b = a.groupBy('code')
# b.execFunc('scale','price')
# a[0].setName('Ji')
# a[4].setCode('haha')
# filter = a.filter(lambda x:x.code.find('77')!=-1)
# a.join(k,'sameCode',lambda left,right:left.code.find('5')!=-1 and right.code.find('2')!=-1)
# result = a.filter(lambda x:x.sameCode)
# a.scale('price','haha',inplace=True)
# c = a.groupBy('name')
# b = a.execFunc('run','shir')
# buildAttr(path+os.sep+'test.xlsx')
# clearAttr()

# from RiskQuantLib.Module import *
# # buildAttr(path+os.sep+'test.xlsx')
# a = stockList()
# k = bondList()
# a.addStockSeries(['code_'+str(int(i/2)) for i in range(100)],['a_'+str(i) for i in range(100)])
# k.addBondSeries(['code_'+str(int(i/3)) for i in range(100)],['k_'+str(i) for i in range(100)])
# a.setIssuerName(['code_'+str(i) for i in range(100)],['issuer_'+str(i) for i in range(100)])
# k.setPrice(['code_'+str(i) for i in range(100)],[i*2 for i in range(100)])
#
# result = a.merge(k,'outer',lambda x,y:x.code==y.code)
# a = securityList()
# a.addSecuritySeries(['a_'+str(int(i/2)) for i in range(1000)],['name'+str(int(i/2)) for i in range(1000)])
# b = securityList()
# b.addSecuritySeries(['a_'+str(int(i/30)) for i in range(1000)],['name'+str(int(i/30)) for i in range(1000)])
#
# a.setIssuer(['a_'+str(int(i/2)) for i in range(1000)],['issuer'+str(int(i/2)) for i in range(1000)])
# b.setIssuer(['a_'+str(int(i/30)) for i in range(1000)],['issuer'+str(int(i/30)) for i in range(1000)])
#
# com = companyList()
# com.addCompanyFromSecurityList(b)
# com.addCompanyFromSecurityList(a)
# com.sort('code',inplace=True)
# print(sum(len(i) for i in com['issuedSecurityList']))
# a.connect(com,"issuerObj","securityIssuedFromA",unsymmetrical=True,filterFunctionOnLeft=lambda x,y:x.issuer==y.code,filterFunctionOnRight= lambda x,y:x.issuer==y.code)
# b.connect(com,"issuerObj","securityIssuedFromB",unsymmetrical=True,filterFunctionOnLeft=lambda x,y:x.issuer==y.code,filterFunctionOnRight= lambda x,y:x.issuer==y.code)
# s0 = a['name',]
# s1 = a['code',lambda x:x.find('6')!=-1]
# s2 = a['issuerObj',:]
# s3 = a['issuerObj',0]
# s4 = a.groupBy('code')['all',:]
# from RiskQuantLib.Tool.pptTool import formatPpt
# df = pd.DataFrame([[1,2,3],[4,5,6]],index=['A','B'],columns=['alpha','beta','gamma'])
# formatPpt(path+os.sep+'test.pptx',path+os.sep+'res.pptx',tableDict={0:df},textDict={'{hu}':'shit','{title}':'I just want to be a man or hero','{subtitle}':"just this dream"},graphDict={0:path+os.sep+"a.png"})

# from RiskQuantLib.Tool.githubTool import Github
# link = Github()
# link.downloadRepositories("https://github.com/SyuyaMurakami/RiskQuantLib",path)
# from RiskQuantLib.Module import *
# a = stockList()
# k = bondList()
# a.addStockSeries(['code_'+str(int(i/2)) for i in range(100)],[int(i/3) if i%5!=0 else np.nan for i in range(100)])
# k.addBondSeries(['code_'+str(int(i/3)) for i in range(100)],['k_'+str(i) for i in range(100)])
# b= a[1]
# c = a.sort(['name','code'],inplace=True,reverse=True)
# b.assdas='aas'
# d = a[:2]
# d[0].stock = k[:2]
# d[1].stock = k[2:4]
# k[0].bond = [1,2,3]
# k[1].bond = [4,5,6]
# k[2].bond = [1,2,3]
# k[3].bond = [4,5,6]

# a = stockList()
# a.addStockSeries(['code_'+str(i) for i in range(1000000)],[int(i) for i in range(1000000)])
# value = np.linspace(0,len(a),len(a)+1)
# time0 = time.time()
# a.updateAttr('shit',a['code'],np.linspace(0,len(a),len(a)+1))
# print("用时：",time.time()-time0)
# a.addStock('dhasi','asdjha')
# a.updateAttr('shit',['a','c'],[45,56])
# b = a.toArray('shit') + 23
# a.updateAttrFromArray(b,a['name'],'shitPlus',byAttr='name')
# time1 = time.time()
# a.apply(lambda x:x.shit**2+x.shitPlus**5 - x.shit**3)
# print("用时：",time.time()-time1)
#
# time2 = time.time()
# fg = a.toArray('shit')
# gh = a.toArray('shitPlus')
# fg**2+gh**5 - fg**3
# print("用时：",time.time()-time2)

# a = stockList()
# a.addStockSeries(['code_'+str(int(i/3)) for i in range(10000)],[int(i/5) for i in range(10000)])
# a.groupByFunc(lambda x:(x.code,x.name))
# b = a.toDF(['code','name'],attrNameAsIndex='code')
# b['name'] = range(b.shape[0])
# a.updateAttrFromSeries(pd.Series(),'hi')
# a.updateAttrFromSeries(b['name']+9)

# from RiskQuantLib.Tool.fileTool import fileSender,fileReceiver
# send = fileSender(r"C:\Users\xywan\Downloads\Avengers.Endgame.2019.1080p.BluRay.H264.AAC-RARBG.mp4")
# send.run()

# from RiskQuantLib.__init__ import sendProjectTemplate
# sendProjectTemplate()

# if os.path.isfile(path+os.sep+"RiskQuantLib"+os.sep+"Build"+os.sep+'buildInfo.pkl'):
#     buildObj = excelBuilder.loadInfo(path+os.sep+"RiskQuantLib"+os.sep+"Build"+os.sep+'buildInfo.pkl')
# else:
#     buildObj = excelBuilder()
# buildObj.buildProject(instrumentExcelPath=path+os.sep+"Build_Instrument.xlsx",attributeExcelPath=path+os.sep+"Build_Attr.xlsx")
# buildObj.renderProject()


# from RiskQuantLib.Build.builder import excelBuilder
# bd = excelBuilder(targetProjectPath=r'C:\Users\xywan\OneDrive - SAIF\桌面\RQL2\Test')
# bd = excelBuilder.loadInfo(r'C:\Users\xywan\OneDrive - SAIF\桌面\RQL2\Test')
# bd.buildProject(r'C:\Users\xywan\OneDrive - SAIF\桌面\RQL2\Test'+os.sep+'Build_Instrument.xlsx',r'C:\Users\xywan\OneDrive - SAIF\桌面\RQL2\Test'+os.sep+'Build_Attr.xlsx')
# bd.renderProject(k = 'fuck',instantUpdate=True)
# bd.clearProject()

# from RiskQuantLib.Tool.fileTool import dirWatcher
# a = dir([r'C:\Users\xywan\OneDrive - SAIF\桌面\RQL2\Test\Src'])
# a.start()

# from RiskQuantLib.Tool.fileTool import systemWatcher
# a = systemWatcher([r'C:\Users\xywan\OneDrive - SAIF\桌面\RQL2\Test\ji.txt',r'C:\Users\xywan\OneDrive - SAIF\桌面\RQL2\Test\h.txt',r'C:\Users\xywan\OneDrive - SAIF\桌面\RQL2\Test\Src'],call_back_function_on_any_change=lambda x:print(x))
# # a = dirWatcher([r'C:\Users\xywan\OneDrive - SAIF\桌面\RQL2\Test\Src',r'C:\Users\xywan\OneDrive - SAIF\桌面\RQL2\Test\Build'])
# a.start()

# from RiskQuantLib import persistProject,buildProject,unBuildProject
# buildProject(r'C:\Users\xywan\OneDrive - SAIF\桌面\RQL2\Test')
# persistProject(r'C:\Users\xywan\OneDrive - SAIF\桌面\RQL2\Test')
# unBuildProject(r'C:\Users\xywan\OneDrive - SAIF\桌面\RQL2\Test')

# from RiskQuantLib import packProject
# packProject(r"C:\Users\xywan\Downloads\疾速备战.720p.1080p.BD中英双字")

from RiskQuantLib import listProjectTemplate, unpackProject
listProjectTemplate()
unpackProject('4',r"C:\Users\xywan\OneDrive - SAIF\桌面\RiskQuantLib2\src\Test")
print()
