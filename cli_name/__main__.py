import sys
import pandas as pd
import os
import numpy as np
import click
from .functions import my_class

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
def Print(path,out=None,parsedatasource=True,parsefields=False):
    print(path)

if __name__ == '__main__':
    main()
