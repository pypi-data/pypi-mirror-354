import click
from haplohub import GetVariantRequest, VariantRange

from haplohub_cli.core.api.client import client


@click.group()
def variant():
    """
    Work with variants
    """
    pass


@variant.command()
@click.option("--sample_id", "-s", type=int, required=True)
@click.option("--accession", "-a", type=str, required=True)
@click.option("--start", "-st", type=int, required=True)
@click.option("--end", "-e", type=int, required=True)
@click.option("--cohort", "-c", type=str, required=True)
def fetch(sample_id: str, accession: str, start: int, end: int, cohort: str):
    request = GetVariantRequest(
        sample_id=sample_id,
        variants=[
            VariantRange(
                accession=accession,
                start=start,
                end=end,
            )
        ],
    )

    return client.variant.get_variant(cohort, request)
