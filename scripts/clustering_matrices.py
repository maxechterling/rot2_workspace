#!/usr/bin/env python

"""
Usage:
./clustering_matrices.py synapse_by_neuron.txt
"""

import sys
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

def split_coord( coord ):
    coord = coord.lstrip('(').rstrip(')').split()
    return map( float, coord )
    
def extend_neuron_df( neuro_df ):
    extended = []
    for entry in neuro_df.values:
        for synapse in entry[1].split(','):
            extended.append( [ entry[0], synapse, entry[2] ])
    return pd.DataFrame( extended, columns=['coord', 'partner', 'type'] )

def read_synapse_by_neuron( filt_typ ):
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
                    df = pd.DataFrame( {'partner': syn_names, 'type': syn_type, \
                                                    'coord': coords} )
                    neuro_dic[ key ] = extend_neuron_df( df[ df.type == filt_typ ] )\
                                       .sort_values( by='partner' ).set_index( keys='partner' )
                else:
                    pass
    return neuro_dic
    
def read_adj_order( neurons ):
    with open( sys.argv[2] ) as f:
        count, adj_lst, final_lst = 0, [], []
        for line in f:
            if count == 0 or count == 1:
                count += 1
            elif line.lstrip(',,').rstrip(',\r\n').split(',')[3] == 'I2R':
                break
            else:
                adj_lst.append( line.rstrip(',\r\n').split(',')[1] )
        for neuron in adj_lst:
            if neuron in set( neurons ):
                final_lst.append( neuron )
        return final_lst

def convert_coord_lst( coords ):
    converted = []
    if type( coords ) == list:
        converted.append( coords )
    else:
        for coord in coords:
            converted.append( coord )
    return np.array( converted )
    
def clustering_score_by_neuron( neuron, dic1, dic2 ):
    total_syn, scores = len( dic1[ neuron] ), []
    for n1 in list( set( dic1[ neuron ].index ) ):
        n1_df = dic1[ neuron ].loc[ n1 ]['coord']
        for n2 in list( set( dic2[ neuron ].index ) ):
            if n1 == n2:
                pass
            else:
                n2_df = dic2[ neuron ].loc[ n2 ]['coord']
                paired_dist = cdist( convert_coord_lst( n1_df ), convert_coord_lst( n2_df ) )
                summed = sum( [ sum( x ) for x in paired_dist ] )
                n = sum( [len( x ) for x in paired_dist ] )
                score = n / np.log( summed / n )
                scores.append( score )
    if total_syn != 0 or len( scores ) != 0:
        print scores, total_syn
        print sum( scores ) / total_syn
    else:
        print 0
    
def main():
    pre_dic, post_dic = read_synapse_by_neuron( 'pre' ), read_synapse_by_neuron( 'post' )
    adj_order = read_adj_order( pre_dic.keys() )
    clustering_dic = {}
    for neuron in adj_order:
        clustering_dic[ neuron ] = clustering_score_by_neuron( neuron, pre_dic, pre_dic )
    plt.figure()
    print clustering_dic.values()
    plt.hist( clustering_dic.values() )
    plt.show()
    plt.close()
        
        
    
main()
