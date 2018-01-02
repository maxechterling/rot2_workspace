#!/usr/bin/env python

"""

Usage:
./link_analysis.py dist.link adjacency.csv

"""

import sys
import pandas as pd
from itertools import izip

def read_link( link ):
    neuron_dic = {}
    with open( link ) as f:
        first = True
        matrix = []
        for line in f:
            if line.startswith( '##' ):
                neurons = line.lstrip('##COLUMNS: ').rstrip('\r\n').split(', ')
            elif line.startswith( '>' ) and first is True:
                first = False
                key = line.lstrip('>').rstrip('\r\n')
            elif line.startswith( '>' ) and first is False:
                neuron_dic[ key ] = pd.DataFrame( matrix, columns=neurons, index=neurons )
                key = line.lstrip('>').rstrip('\r\n')
                matrix = []
            elif line.startswith( 'END' ):
                neuron_dic[ key ] = pd.DataFrame( matrix, columns=neurons, index=neurons )
            else:
                matrix.append( line.rstrip('\r\n').split(', ') )
    return neuron_dic

def sum_distances( dist_dic ):
    first = True
    for neuron, df in dist_dic.items():
        df = df.astype('float').fillna( value=0 )
        if first is True:
            master_df = df
            first = False
        else:
            master_df.add( df )
    return master_df
    
def read_adj_matrix():
    adj_matrix = []
    with open( sys.argv[2] ) as f:
        rows, count = [], 0
        for line in f:
            if count == 0:
                count += 1
            elif count == 1:
                columns = line.split(',')[2:-1]
                count += 1
            elif line.split(',')[4] == 'I2L':
                break
            else:
                rows.append( line.split(',')[1] )
                adj_matrix.append( line.split(',')[2:-1] )
    return pd.DataFrame( adj_matrix, columns=columns, index=rows )
                
def align_dataframes( master_df, adj_df ):
    master_neurons, adj_c, adj_r = set( master_df.columns ), set( adj_df.columns ), \
                                   set( adj_df.index )
    neurons_oi = list( adj_c & adj_r & master_neurons )
    return master_df[ neurons_oi ].reindex( neurons_oi ), adj_df[ neurons_oi ].reindex( neurons_oi )
    
def merged_output( master_df, adj_df ):
    for master, adj in izip(master_df.values, adj_df.values):
        merged_line = []
        for i in range( len( master ) ):
            if master[i] == 0:
                merged_line.append( '' )
            
        ## TODO: finish
                              
def main():
    dist_dic = read_link( sys.argv[1] )
    master_df = sum_distances( dist_dic )
    adj_df = read_adj_matrix()
    master_df, adj_df = align_dataframes( master_df, adj_df )
    merged_output( master_df, adj_df )
    
main()
