#!/usr/bin/env python

"""
"""

import sys
import numpy as np
from numpy.linalg import norm
import pandas as pd
import matplotlib.pyplot as plt
import math

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
    
def intra_neuro_distances( neuron_df, filter_type1, filter_type2 ):
    distances = []
    if filter_type1 != 'all':
        neuro1_lst = neuron_df.where( neuron_df['type'] == filter_type1 ).dropna()[['coord']].values
    else: 
        neuro1_lst = neuron_df[['coord']].values
    if filter_type2 != 'all':
        neuro2_lst = neuron_df.where( neuron_df['type'] == filter_type2 ).dropna()[['coord']].values
    else: 
        neuro2_lst = neuron_df[['coord']].values
    for coord in neuro1_lst:
        dist = nearest_neighbor( coord, neuro2_lst )
        if dist == None:
            pass
        else:
            if math.isnan( dist ) == True:
                pass
            elif dist == 500000:
                pass
            else:
                distances.append( dist )
    return distances
                              
def nearest_neighbor( coord, coord_lst ):
    dist_lst = []
    for coord2 in coord_lst:
        if len( coord2[0] ) < 3:
            dist_lst.append( 500000 )
        elif coord[0][0] == coord2[0][0] and coord[0][1] == coord2[0][1] and coord[0][2] == coord2[0][2]:
            dist_lst.append( 500000 )
        elif coord != coord2:
            dist_lst.append( norm( coord[0] - coord2[0] ) )
    if len(dist_lst) == 0:
        pass
    else:
        return min( dist_lst )
            
def plot_histogram( dist_list, comboes, out_name=None ):
    plt.figure()
    for combo in comboes:
        plt.hist( dist_list[ combo ], bins=100, alpha=0.6, label=combo, histtype='step' )
    plt.xlabel( 'log10( distance )' )
    plt.ylabel( 'counts' )
    plt.legend()
    if out_name is None:
        plt.show()
    else:
        plt.savefig( out_name )
    plt.close()
    
def transform_dist( distances ):
    logged = []
    for each in distances:
        logged.append(  np.log( each ) )
    return logged
        
def main():
    neuro_dic = read_synapse_by_neuron()
    combos = [ 'pre_pre', 'pre_post', 'post_post', 'all_all', 'post_pre', 'gap_gap', 'pre_gap', 'post_gap', 'pre_all', 'post_all', 'gap_all' ]
    dist_dic = {}
    for combo in combos:
        type1, type2 = combo.split('_')[0], combo.split('_')[1]
        dist_dic[ combo ] = []
        for neuron in neuro_dic.keys():
            dist_dic[ combo ] = dist_dic[ combo ] + intra_neuro_distances( neuro_dic[ neuron ], type1, type2 )
        dist_dic[ combo ] = transform_dist( dist_dic[ combo ] )
    #plot_histogram( dist_dic, [ 'pre_pre', 'pre_post', 'all_all', 'gap_gap', 'post_post', 'post_pre', 'pre_gap', 'post_gap' ] )
    plot_histogram( dist_dic, [ 'pre_all', 'post_all', 'gap_all' ], 'synapse_to_all.png' )
    plot_histogram( dist_dic, [ 'pre_pre', 'pre_post', 'post_post' ] )
    
    
main()