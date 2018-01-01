#!/usr/bin/env python

"""

Usage:
./3d_hist.py synapse_by_neuron.txt

"""

import sys
import pandas as pd
import numpy as np
import math
from itertools import product


def read_coords():
	coords = []
	with open( sys.argv[1] ) as f:
		for line in f:
			if line.startswith('('):
				line = line.rstrip('\r\n').split('\t')
				for coord in line:
					coords.append( [ float( each ) for each in \
								  coord.lstrip('(').rstrip(')').split() ] )
	return pd.DataFrame( coords, columns=[ 'x', 'y', 'z' ] )

def find_bounds( coords_df, xbin, ybin, zbin ):
	x_max, y_max, z_max = coords_df['x'].max(), coords_df['y'].max(), \
				          coords_df['z'].max()
	x_min, y_min, z_min = coords_df['x'].min(), coords_df['y'].min(), \
				          coords_df['z'].min()
	x_min, x_max = math.floor( x_min / xbin ) * xbin, math.ceil( x_max / xbin ) * xbin
	y_min, y_max = math.floor( y_min / ybin ) * ybin, math.ceil( y_max / ybin ) * ybin
	z_min, z_max = math.floor( z_min / zbin ) * zbin, math.ceil( z_max / zbin ) * zbin
	return [ x_min, x_max, y_min, y_max, z_min, z_max ]

def loop_thru_bins( min, max, b_size ):
	bin_coords = []
	for i in range( min, max + b_size, b_size ):
		bin_coords.append( i )
	return bin_coords

def init_bin_dic( bounds, xbin, ybin, zbin ):
    xyz = []
    bin_dic = {}
    xyz.append( loop_thru_bins( int( bounds[0] ), int( bounds[1] ), xbin ) )
    xyz.append( loop_thru_bins( int( bounds[2] ), int( bounds[3] ), ybin ) )
    xyz.append( loop_thru_bins( int( bounds[4] ), int( bounds[5] ), zbin ) )
    for coord in list( product( *xyz ) ):
        bin_dic[ ' '.join( [ str(num) for num in coord ] ) ] = 0
    return bin_dic

def round_coords( coords_df, xbin, ybin, zbin ):
    coords_df['x'] = coords_df['x'] / xbin
    coords_df['x'] = coords_df['x'].round() * xbin
    coords_df['y'] = coords_df['y'] / ybin
    coords_df['y'] = coords_df['y'].round() * ybin
    coords_df['z'] = coords_df['z'] / zbin
    coords_df['z'] = coords_df['z'].round() * zbin
    return coords_df.dropna()

def count_hits( rounded_df, bin_dic ):
    for coord in rounded_df.values:
        coord_key = ' '.join( [ str(int(num)) for num in coord ] )
        bin_dic[ coord_key ] += 1
    return bin_dic

def make_output_df( bin_dic ):
    combined = []
    for key, value in bin_dic.items():
        if value != 0:
            coord = key.split()
            coord.append( value )
            combined.append( coord )
    return pd.DataFrame( combined, columns=[ 'x', 'y', 'z', 'count' ] )
    
def main():
    xbin, ybin, zbin = 500, 500, 500
    coords_df = read_coords()
    bounds = find_bounds( coords_df, xbin, ybin, zbin )
    bin_dic = init_bin_dic( bounds, xbin, ybin, zbin )
    rounded_df = round_coords( coords_df, xbin, ybin, zbin )
    bin_dic = count_hits( rounded_df, bin_dic )
    output_df = make_output_df( bin_dic )
    output_df.to_csv( 'density_3d.csv', header=False, index=False )
    
main()