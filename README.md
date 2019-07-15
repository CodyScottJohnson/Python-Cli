# Tableau Data Scraper
Simple kind of ugly utilitiy to loop through a folder full of tableau workbooks and output basic information about the datasources used in the workbook.

The file returns 4 csv with the following info
### *WorkBookInfo.csv*
>Info on each workbook contained in the source folder
<details>
    <summary>1. DatasourceName</summary>
       
        
 </details>
 <details>
    <summary>2. Connections</summary>
        <p>comma delimited list of connections used in the format (Database: [name of database]  Server: [Server URL])</p>
        
 </details>
 <details>
    <summary>3. Tables</summary>
        <p>comma delimited list of tables used in the workbook in the format [database].[connection].[table] </p>
        
 </details>
 <details>
    <summary>4. SqlQuery-[1-n]</summary>
        <p>There will be a column for each unique SQL Query in the workbook (i.e. SqlQuery-1, SqlQuery-2 etc) containing the text of the query with a use [database]; statement appended to the front</p>
        
 </details>

 ### *DatasourceInfo.csv*
 > Info on Tableaus datasources `.tdsx` & .`tds` these datasource are often referenced in the other files so this file provides a breakdown of the tables and connections contained in those datasources
<details>
    <summary>1. Workbook Name</summary>
       
        
 </details>
 <details>
    <summary>2. Connections</summary>
        <p>comma delimited list of connections used in the format (Database: [name of database]  Server: [Server URL])</p>
        
 </details>
 <details>
    <summary>3. Tables</summary>
        <p>comma delimited list of tables used in the datasource in the format [database].[connection].[table] </p>
        
 </details>
 <details>
    <summary>4. SqlQuery-[1-n]</summary>
        <p>There will be a column for each unique SQL Query in the datasource (i.e. SqlQuery-1, SqlQuery-2 etc) containing the text of the query with a use [database]; statement appended to the front</p>
        
 </details>

### *Table_Counts.csv*
>Summary info on each table used in any workbook
<details>
    <summary>1. Tables</summary>
    <p>Name of the table in the format [database].[connection].[table]</p>
       
        
 </details>
 <details>
    <summary>2. Workbooks</summary>
        <p>comma delimited list of workbooks that use the table in any way</p>
        
 </details>
 <details>
    <summary>3. # of Workbooks</summary>
        <p>count of how many workbooks use the table in some way</p>
        
 </details>

### *Connection_Counts.csv*
>Summary info on each connection used in any workbook
<details>
    <summary>1. Connections</summary>
    <p>Name of the connection</p>
       
        
 </details>
 <details>
    <summary>2. Workbooks</summary>
        <p>comma delimited list of workbooks that use the connection in any way</p>
        
 </details>
 <details>
    <summary>3. # of Workbooks</summary>
        <p>count of how many workbooks use the connection in some way</p>
        
 </details>
 
csv is output into the current directory by default

## Setup
>Install Command Line Tool
```bash
make install
```
>Remove Command Line Tool
```bash
make uninstall
```
## Usage
```
tableau-scraper [command] [-paramaters]
```
### Commands

**Parse**
```
tableau-scraper parse -p "path to workbooks"
```
##### options
flag | default|description
--|--|--
`-p, --path` |No Default (Required)| Directory containing tableau workbooks
`-o, --out` |Current Directory| Directory to output results
`-pd, --parseDatasource` |True| Parse Datasource files .tds .tdsx, they take longer to parse to you may consider skipping to save time

## help
```
tableau-scraper --help
```

## Development
```bash
make install-dev
```
Installs the package in development mode so that changes you make to the source will be immedietly reflected when calling ```tableau-scraper```