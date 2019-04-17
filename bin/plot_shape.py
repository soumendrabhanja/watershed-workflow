#!/usr/bin/env python3
"""Plots watersheds and their context within a HUC.
"""
import os,sys
import logging
import numpy as np
from matplotlib import pyplot as plt
import shapely

import workflow.hilev
import workflow.ui
import workflow.files
import workflow.plot


if __name__ == '__main__':
    parser = workflow.ui.get_basic_argparse(__doc__)
    workflow.ui.inshape_args(parser)
    workflow.ui.huc_hint_options(parser)
    workflow.ui.huc_source_options(parser)
    workflow.ui.center_options(parser)

    args = parser.parse_args()
    workflow.ui.setup_logging(args.verbosity, args.logfile)


    args.source_hydro = args.source_huc
    args.source_huc = 'NHD WBD' # hard-coded, but need to use the full WBD dataset
    sources = workflow.files.get_sources(args)

    # collect data
    # -- collect shape of interest
    profile, watersheds, watershed_boundary, centroid = \
                workflow.hilev.get_shapes(args.infile, args.shape_index, False, make_hucs=False)

    # -- find and collect containing huc
    hucstr = workflow.hilev.find_huc(profile, watershed_boundary, sources['HUC'], args.hint)
    logging.info("found shapes in HUC %s"%hucstr)
    hucs, centroid = workflow.hilev.get_hucs(hucstr, sources['HUC'])

    # -- find and center rivers
    rivers = workflow.hilev.get_rivers(hucstr, sources['Hydro'])
    rivers = [shapely.affinity.translate(r, -centroid.coords[0][0], -centroid.coords[0][1]) for r in rivers]

    # -- center shape
    watersheds = [shapely.affinity.translate(shp, -centroid.coords[0][0], -centroid.coords[0][1]) for shp in watersheds]
    watershed_boundary = shapely.affinity.translate(watershed_boundary, -centroid.coords[0][0], -centroid.coords[0][1])        
        
    # plot
    workflow.plot.hucs(hucs, color='k')
    bounds = shapely.ops.cascaded_union(list(hucs.polygons())).bounds
    plt.text(bounds[0], bounds[1], hucstr)

    workflow.plot.shapes(watersheds, color='r')
    workflow.plot.rivers(rivers, color='b')
    plt.show()
    #for i, ws in enumerate(watersheds.polygons()):
        

    
    
    
