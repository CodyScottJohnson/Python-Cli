# Python Cli Template

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