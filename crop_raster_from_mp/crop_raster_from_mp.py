#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 12:03:18 2022

@author: quentin
"""
import click
import geopandas as gpd
import glob
import logging
import numpy as np
import os
import rasterio
import rasterio.mask
import shapely.geometry
from shapely.geometry import Polygon
import shutil

LOGGER = logging.getLogger('crop_raster_mp')


def crop_raster_from_mp(microplot_in, raster_in, attribute, output_folder):
    
    out_folder_tif = os.path.join(output_folder,'tif')
    os.mkdir(out_folder_tif)
    #output_folder_zip = os.path.join(output_folder,'zip')
    
    LOGGER.info(f'Read raster {raster_in}')
    raster = rasterio.open(raster_in)
    crs = int(raster.crs.to_string().split(':')[1])
    LOGGER.info(f'EPSG code of raster CRS is {crs}')
    
    LOGGER.info(f'Read vector {microplot_in}')
    gdf_mp = gpd.read_file(microplot_in)

    LOGGER.info(f'Check CRS vector')
    if gdf_mp.crs.to_epsg() == crs:
        gdf_mp_utm = gdf_mp
    else:
        gdf_mp_utm = gdf_mp.to_crs(crs)
    
    # Iterate on geometries
    LOGGER.info(f'Create tif from microplots')
    with rasterio.open(raster_in) as src:
        for index, row in gdf_mp_utm.iterrows():
            coordinates = np.array(row['geometry'].exterior.coords)
            coordinates = coordinates[:, :2]
            output_polygon = Polygon(coordinates)
            geom = [shapely.geometry.mapping(output_polygon)]
            out_image, out_transform = rasterio.mask.mask(src, geom, crop=True)
            out_meta = src.meta
            out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})
            with rasterio.open(os.path.join(out_folder_tif,row[attribute]+'.tif'), "w", **out_meta) as dest:
                dest.write(out_image)
    
    LOGGER.info(f'Create archive of microplots')
    shutil.make_archive(out_folder_tif,
                        'zip',
                        output_folder,
                        base_dir='./tif')
