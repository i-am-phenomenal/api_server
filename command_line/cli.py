import click 
import utils

@click.group()
def cli():
    pass

@cli.command()
def listalldatasets(): 
    utils.getAllDatasets()

@cli.command()
@click.argument("datasetid", type=int)
def getdataset(datasetid):
    utils.getDatasetByDatasetId(datasetid)

cli()