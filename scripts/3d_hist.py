#!/usr/bin/env python

"""

Usage:
./3d_hist.py synapse_by_neuron.txt

"""

import sys
import pandas as pd
import numpy as np
import math


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
	bin_dic = {}
	x = loop_thru_bins( int( bounds[0] ), int( bounds[1] ), xbin )
	print len(x)


def main():
	xbin, ybin, zbin = 500, 500, 1000
	coords_df = read_coords()
	bounds = find_bounds( coords_df, xbin, ybin, zbin )
	bin_dic = init_bin_dic( bounds, xbin, ybin, zbin )
	#np.histogramdd( np.array( coords_df.values ) )


main()