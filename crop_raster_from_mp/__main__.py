import click
import logging

from crop_raster_from_mp.crop_raster_from_mp import crop_raster_from_mp


LOGGER = logging.getLogger(__name__)


@click.command()
@click.option("-imp", "--microplot_in", "microplot_in", type=str,
              help='Input microplots path')
@click.option("-ir", "--raster_in", "raster_in", type=str,
              help='Input raster path')
@click.option("-a", "--attribute", "attribute", type=str,
              help='Attribute with unique IDs to identify clipped microplot')
@click.option("-of", "--output_folder", "output_folder", type=str,
              help='Output folder for microplots extraction')
def cli(
    microplot_in,
	raster_in,
    attribute,
	output_folder
	):

    LOGGER.info("Launch the algo")

    crop_raster_from_mp(
        microplot_in,
        raster_in,
        attribute,
        output_folder
        )

    LOGGER.info("Finished")


if __name__ == "__main__":
    cli()
