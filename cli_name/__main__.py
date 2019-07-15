import sys
from tableaudocumentapi import Workbook
from collections import OrderedDict 
import pandas as pd
import os
import numpy as np
import click
from .tableau_functions import dbx_tableau 
from .sql_parser import sqlParser 

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        Parse()

@main.command(help="Pull datasource info from a directory of .twb .twbx .tds .tdsx files")
@click.option("--path","-p", prompt="Workbook Directory",help="Directory containing tableau workbooks")
@click.option("--out","-o",help="Directory to output results")
@click.option("--parseDatasource","-pd",help="Parse Datasource files .tds .tdsx",type=bool, default=True)
@click.option("--parseFields","-pf",help="Parse Datasource Fields",type=bool, default=False)
@click.version_option()
def Parse(path,out=None,parsedatasource=True,parsefields=False):
    Output = []
    TableauSources = []
    Workbooks = []
    WorkbookConnection = []
    sourceDir = path or "./"
    outputDir = out or "./"
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    numFiles = len(os.listdir(sourceDir))
    print()
    dbx_tableau.printProgressBar(0, numFiles, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i,file in enumerate(os.listdir(sourceDir)):
        filename = os.fsdecode(file)
        if filename.endswith(".twb") or filename.endswith(".twbx"): 
            sourceWB = Workbook(os.path.join(sourceDir, filename))
            connections, tables, sqlQueries, fields = dbx_tableau.parseTableauFile(sourceWB,parsefields)
            WorkbookInfo = OrderedDict({
                                    'WorkbookName': filename,
                                    'Workday': dbx_tableau.checkWorkday(tables),
                                    'Greenhouse': dbx_tableau.checkGreenhouse(tables),
                                    'Glint': dbx_tableau.checkGlint(tables),
                                    'Redcat': dbx_tableau.checkRedcat(tables),
                                    'Reflective': dbx_tableau.checkReflective(tables),
                                    'Connections': ",".join(connections),
                                    'Tables': ",".join(tables),
                                    'Fields': ",".join(fields),
                                    **sqlQueries
                                    })
            if not parsefields:
                del WorkbookInfo["Fields"]
            Output.append(WorkbookInfo)
            for table in tables:
                Workbooks.append({'WorkbookName': filename,"Table":table})
            for connection in connections:
                WorkbookConnection.append({'WorkbookName': filename,"Connection":connection})
            dbx_tableau.printProgressBar(i+1, numFiles, prefix = 'Progress:', suffix = 'Complete', length = 50)
            continue
        if filename.endswith(".tdsx") and parsedatasource:
            TableauSources += dbx_tableau.readDatasourceTsdx(os.path.join(sourceDir, filename))
            dbx_tableau.printProgressBar(i+1, numFiles, prefix = 'Progress:', suffix = 'Complete', length = 50)
            continue
        if filename.endswith(".tds") and parsedatasource:
            TableauSources.append(dbx_tableau.readDatasourceTds(os.path.join(sourceDir, filename)))
            dbx_tableau.printProgressBar(i+1, numFiles, prefix = 'Progress:', suffix = 'Complete', length = 50)
        else:
            continue
    print()    
    
    #Save Workbook Info
    data = pd.DataFrame(Output)
    data.to_csv(os.path.join(outputDir,'WorkBookInfo.csv'),index=False)
    #Save Datasource Info
    data = pd.DataFrame(TableauSources)
    data.to_csv(os.path.join(outputDir,'DataSourceInfo.csv'),index=False)

    #Count how many workbooks use each table     
    df = pd.DataFrame(Workbooks)   
    table = df.Table.apply(pd.Series) \
        .merge(df, right_index = True, left_index = True) \
        .drop(["Table"], axis = 1) \
        .melt(id_vars = ['WorkbookName'], value_name = "Tables") \
        .drop(["variable"], axis = 1) \
        .dropna()
    names = table.groupby(['Tables'])['WorkbookName'].apply(','.join).to_frame().reset_index()
    names.columns = ['Tables','Workbooks']
    counts = table.groupby(['Tables']).count().reset_index()
    counts.columns = ['Tables','# of Workbooks']
    TableCounts = names.merge(counts,on="Tables").sort_values(['# of Workbooks'], ascending=False)
    TableCounts.to_csv(os.path.join(outputDir,'Table_Counts.csv'),index=False)




    #Count how many workbooks use each connection     
    df = pd.DataFrame(WorkbookConnection)   
    table = df.Connection.apply(pd.Series) \
        .merge(df, right_index = True, left_index = True) \
        .drop(["Connection"], axis = 1) \
        .melt(id_vars = ['WorkbookName'], value_name = "Connections") \
        .drop(["variable"], axis = 1) \
        .dropna()
    names = table.groupby(['Connections'])['WorkbookName'].apply(','.join).to_frame().reset_index()
    names.columns = ['Connections','Workbooks']
    counts = table.groupby(['Connections']).count().reset_index()
    counts.columns = ['Connections','# of Workbooks']
    ConnectionCounts = names.merge(counts,on="Connections").sort_values(['# of Workbooks'], ascending=False)
    ConnectionCounts.to_csv(os.path.join(outputDir,'Connection_Counts.csv'),index=False)

    #Output Workbook Info
    data = pd.DataFrame(Output)
    data.to_csv(os.path.join(outputDir,'WorkBookInfo.csv'),index=False) 


@main.command()
@click.option("--path","-p", prompt="Workbook Directory",help="Directory containing tableau workbooks")
@click.option("--out","-o",help="Directory to output results")
@click.option("--parseDatasource","-pd",help="Parse Datasource files .tds .tdsx",type=bool, default=True)
def Test(path,out=None,parsedatasource=True):
    sourceDir = path or "./"
    outputDir = out or "./"
    numFiles = len(os.listdir(sourceDir))
    print()
    #dbx_tableau.printProgressBar(0, numFiles, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i,file in enumerate(os.listdir(sourceDir)):
        filename = os.fsdecode(file)
        if filename.endswith(".twb") or filename.endswith(".twbx"): 
            sourceWB = Workbook(os.path.join(sourceDir, filename))
        for db in sourceWB.datasources:
            dbx_tableau.getFieldInfo(db)
    print()    

if __name__ == '__main__':
    main()
