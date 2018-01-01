#!/usr/bin/env python

"""

Usage:
./3d_clusters.py synapse_by_neuron.txt

"""

import sys
import pandas as pd
import numpy as np

def split_coord( coord ):
    coord = coord.lstrip('(').rstrip(')').split()
    return np.array( map( float, coord ) )
    
def read_synapse_by_neuron():
    neuro_dic, count = {}, 0
    with open( sys.argv[1] ) as f:
        for line in f:
            count += 1
            if line.startswith('>'):
                key, count = line.lstrip('>').rstrip('\n'), 1
            elif count == 2:
                syn_names = line.rstrip('\n').split('\t')
            elif count == 3:
                syn_type = line.rstrip('\n').split('\t')
            else:
                coords = line.rstrip('\n').split('\t')
                coords = [ split_coord( coord ) for coord in coords ]
                if len(syn_names) == len(syn_type) and len(syn_type) == len(coords):
                    neuro_dic[ key ] = pd.DataFrame( {'partner': syn_names, 'type': syn_type, \
                                                    'coord': coords} )
                else:
                    pass
    return neuro_dic
    
def extend_neuron_df( neuro_dic ):
    extended_dic = {}
    for neuron in neuro_dic.keys():
        extended = []
        for entry in neuro_dic[ neuron ].values:
            for synapse in entry[1].split(','):
                extended.append( [ entry[0], synapse, entry[2] ])
        extended_dic[ neuron ] = pd.DataFrame( extended, columns=['coord', 'partner', 'type'] )
    return extended_dic

def get_coords( neuron_dic ):
    x, y, z = [], [], []
    for neuron in neuron_dic.keys():
        for coord in neuron_dic[ neuron ][ 'coord' ].values:
            if len(coord) > 0:
                x.append( coord[0] ), y.append( coord[1] ), z.append( coord[2] )
    return x, y, z
        
    
def main():
    neuron_dic = extend_neuron_df( read_synapse_by_neuron() )
    x, y, z = get_coords( neuron_dic )
    for i in range( len(x) ):
        print '%s,%s,%s' % ( x[i], y[i], z[i] )
    
main()
    
    