import click

from casp.main import CLI
from casp.main import (
    ExtractPipeline,
    TransformPipeline,
    LoadPipeline,
    RunPipeline,
)


@click.group()
def cli():
    """CLI interface for CASP ETL"""


@cli.command()
@click.option("-c", "--config", required=True, help="Configuration file for run")
def extract(config: str):
    cli = CLI(config)
    cli.execute_etl(ExtractPipeline())


@cli.command()
@click.option("-c", "--config", required=True, help="Configuration file for run")
def transform(config: str):
    cli = CLI(config)
    cli.execute_etl(TransformPipeline())


@cli.command()
@click.option("-c", "--config", required=True, help="Configuration file for run")
def load(config: str):
    cli = CLI(config)
    cli.execute_etl(LoadPipeline())


@cli.command()
@click.option("-c", "--config", required=True, help="Configuration file for run")
def run(config: str):
    cli = CLI(config)
    cli.execute_etl(RunPipeline())