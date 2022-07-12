"""
Download S2 reflectance map from AOI
"""

import json
import logging
import os, glob
from pathlib import Path
import shutil
import sys
from crop_raster_from_mp.crop_raster_from_mp import crop_raster_from_mp

LOGGER = logging.getLogger(__name__)


def load_inputs(input_path):
    inputs_desc = json.load(open(input_path))
    inputs = inputs_desc.get('inputs')
    parameters = inputs_desc.get('parameters')
    return inputs, parameters


def main():
    WORKING_DIR = os.getenv('DELAIRSTACK_PROCESS_WORKDIR')
    if not WORKING_DIR:
        raise KeyError('DELAIRSTACK_PROCESS_WORKDIR environment variable must be defined')
    WORKING_DIR = Path(WORKING_DIR).resolve()

    LOGGER.info('Extracting inputs and parameters...')

    # Retrieve inputs and parameters from inputs.json
    inputs, parameters = load_inputs(WORKING_DIR / 'inputs.json')

    # Get info for the inputs
    microplots = inputs.get('microplot_in')
    microplots_path = inputs['microplot_in']['components'][0]['path']
    LOGGER.info('Microplots input: {name!r} (id: {id!r}) in {microplots_path!r}'.format(
        name=microplots['name'],
        id=microplots['_id'],
        microplots_path=microplots_path))

    raster = inputs.get('raster_in')
    raster_path = inputs['raster_in']['components'][0]['path']
    LOGGER.info('Raster dataset: {name!r} (id: {id!r} in {raster_path!r})'.format(
        name=raster['name'],
        id=raster['_id'],
        raster_path=raster_path))

    suffix = parameters.get('suffix')
    LOGGER.info('Suffix is: {name!r} '.format(
        name=suffix))   

    attribute = parameters.get('attribute')
    LOGGER.info('Attribute is: {name!r} '.format(
        name=attribute))  

    # Create the output directory
    LOGGER.info('Creating the output directory')
    outpath = WORKING_DIR

    # Simulate computation
    LOGGER.info('Computing safety report...')
    crop_raster_from_mp(
        microplots_path,
        raster_path,
        attribute,
        outpath
        )

    # Create the outputs file path
    if suffix != None:
        name = 'Clipped_microplots_' + suffix
    else:
        name = 'Clipped_microplots'

    # Create the outputs.json to describe the deliverables and its path
    LOGGER.info('Creating the outputs.json')
    outputs = {
        "outputs": {
            "microplots_raster_zip": {  # Must match the name of deliverable in yaml
                "type": "file",
                "format": "zip",
                "name": name,
                "components": [
                    {
                        "name": "file",
                        "path": os.path.join(str(outpath), 'tif.zip')
                    }
                ]
            },
        },
        "version": "0.1"
    }
    with open(WORKING_DIR / 'outputs.json', 'w+') as f:
        json.dump(outputs, f, indent = 4)

    LOGGER.info('End of processing.')


if __name__ == '__main__':
    main()
