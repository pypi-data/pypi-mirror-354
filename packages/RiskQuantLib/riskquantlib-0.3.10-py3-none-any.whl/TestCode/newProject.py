#!/usr/bin/python
#coding = utf-8


def newProject(path):
    import sys,os,shutil
    import pandas as pd
    RiskQuantLibDictionary = os.path.abspath(__file__).split('RiskQuantLib'+os.sep+'__init__')[0]

    # source_path = os.path.abspath(RiskQuantLibDictionary)+os.sep+r'RiskQuantLib'
    source_path = os.getcwd() + os.sep + r'RiskQuantLib'
    # target_path = os.getcwd()
    # target_path = sys.argv[1]+os.sep+r'RiskQuantLib'
    target_path = path+os.sep+r'RiskQuantLib'

    if not os.path.exists(target_path):
        # 如果目标路径不存在原文件夹的话就创建
        os.makedirs(target_path)

    if os.path.exists(source_path):
        # 如果目标路径存在原文件夹的话就先删除
        shutil.rmtree(target_path)

    shutil.copytree(source_path, target_path)

    # create excel file for build
    df_attr = pd.DataFrame(index = ['SecurityType','AttrName','AttrType']).T
    df_instrument = pd.DataFrame(index = ['InstrumentName','ParentRQLClassName','ParentQuantLibClassName','LibraryName','DefaultInstrumentType']).T
    df_attr.to_excel(path+os.sep+'Build_Attr.xlsx',index=0)
    df_instrument.to_excel(path+os.sep+'Build_Instrument.xlsx',index=0)

    # create build script
    from RiskQuantLib.Tool.codeBuilderTool import pythonScriptBuilder,codeBuilder
    PYB = pythonScriptBuilder()
    PYB.setTitle()
    PYB.setImport('os')
    PYB.setImport('sys')
    PYB.setImport('RiskQuantLib.Build.build','BA',True,'buildAttr')
    PYB.setImport('RiskQuantLib.Build.build', 'BI', True, 'buildInstrument')
    PYB.code = codeBuilder(indent=0)
    PYB.code.add_line('path = sys.path[0]')
    PYB.code.add_line('BA(path + os.sep + "Build_Attr.xlsx")')
    PYB.code.add_line('BI(path + os.sep + "Build_Instrument.xlsx")')
    PYB.writeToFile(path+os.sep+'build.py')

    # create program start point
    PYB = pythonScriptBuilder()
    PYB.setTitle()
    PYB.setImport('os')
    PYB.setImport('sys')
    PYB.code = codeBuilder(indent=0)
    PYB.code.add_line('path = sys.path[0]')
    PYB.code.add_line('print("Write Your Code Here : "+path+os.sep+"main.py")')
    PYB.writeToFile(path+os.sep+'main.py')

    print('New RiskQuantLib Project Created!')


newProject(r"C:\Users\Hugh\OneDrive - SAIF\桌面\a")


