#!/usr/bin/env python

"""

Usage:
./neuron_linker.py synapse_by_neuron.txt

"""

import sys
import pandas as pd
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import math
from sklearn.metrics.pairwise import pairwise_distances
from scipy.spatial.distance import cdist

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

def neuro_list( neuro_dic ):
    neurons = []
    for neuron in neuro_dic.keys():
        if 'blue' in neuron or 'DROP' in neuron or 'glial' in neuron or 'obj' in neuron or 'v' in neuron or 'd' in neuron:
            pass
        else:
            neurons.append( neuron )
    return neurons
    
def subset( neuro_df, type, partner ):
    by_type = neuro_df[ neuro_df['type'] == type ]
    return by_type[ by_type ['partner'] == partner ]

def convert_coord_lst( coords ):
    converted = []
    for coord in coords:
        converted.append( np.array( coord[0] ) )
    return np.array( converted )
    
def score_distance( neuro1, neuro2, neuro_df, pair ):
    if neuro1 == neuro2:
        return 'Nan'
    n1 = np.array( subset( neuro_df, pair[0], neuro1 )[[ 'coord' ]].values )
    if len( n1 ) == 0:
        return 'NaN'
    n2 = np.array( subset( neuro_df, pair[1], neuro2 )[[ 'coord' ]].values )
    if len( n2 ) == 0:
        return 'NaN'
    else:
        n = len( n1 ) * len( n2 )
        pdist = cdist( convert_coord_lst( n1 ), convert_coord_lst( n2 ) )
        score = n / np.log( sum( [ sum( x ) for x in pdist ] ) / n )
        return score

def score_matrix( neurons, neuro_df, neuro_name, pair ):
    print '>%s' % ( neuro_name )
    for n1 in neurons:
        d1 = []
        for n2 in neurons:
            d1.append( score_distance( n1, n2, neuro_df, pair ) )
        print ', '.join( map( str, d1 ) )

def main():
    neuro_dic = extend_neuron_df ( read_synapse_by_neuron() )
    neurons = neuro_list( neuro_dic )
    print '##COLUMNS: %s' % ( ', '.join( neurons ) )
    for neuron in neurons:
        score_matrix( neurons, neuro_dic[ neuron ], neuron, [ 'pre', 'pre' ] )
    print 'END'
    
main()