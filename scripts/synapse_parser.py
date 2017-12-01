#!/usr/bin/env python

"""
Usage:
./synapse_parser.py <sql_file> neuron dimension2
if you don't want to graph a neuron make neuron argument 'None'
dimension 2 is x or y
"""

import sys
from operator import itemgetter
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm


def read_in_data( field, ind_lst ):
    """
    field is a string with the name of the table you want to extract from the sql
    file ind_lst are the indices of the fields you want to extract from the table
    """
    skip = True
    out = []
    with open( sys.argv[1] ) as f:
        for line in f:
            if line.startswith('INSERT INTO'):
                
                if field in line.split()[2]:
                    skip = False
                else:
                    skip = True
            elif skip == False:
                if line == '\n':
                    skip = True
                else:
                    ext = []
                    for i in ind_lst:
                        ext.append( line.rstrip('\r\n').split(', ')[i].lstrip(' \'')\
                            .rstrip('\'').rstrip(',').rstrip(';').rstrip(')')\
                            .lstrip('(') )
                    out.append( ext )
    return out
    
def get_section( full_df ):
    section_dic, section_lst = {}, []
    mapper = read_in_data( 'image', [1,8])
    for line in mapper:
        section_dic[line[0]] = line[1]
    for img in full_df['img_num'].values:
        section_lst.append( int( section_dic[ img ] ) )
    full_df['z'] = pd.DataFrame( section_lst, columns=['z'] )
    del full_df['img_num']
    return full_df
    
def group_contins( full_df ):
    averaged_con = []
    last, x_avg, y_avg, z_avg = 0, None, None, None
    for row in full_df.values:
        if int(row[3]) != last:
            averaged_con.append( [row[0], row[1], row[2], last, x_avg, y_avg, z_avg] )
            last, x_avg, y_avg, z_avg = int(row[3]), int(row[4]), int(row[5]), int(row[6])
        else:
            x_avg = np.mean( [x_avg, int(row[4])] )
            y_avg = np.mean( [y_avg, int(row[5])] )
            z_avg = np.mean( [z_avg, int(row[6])] )
    return pd.DataFrame( averaged_con, columns=['pre','post','type','contin','x','y','z'] )
      
def scale_xyz( grouped_df ):
    grouped_df['x'], grouped_df['y'] = pd.to_numeric( grouped_df['x'] ), pd.to_numeric( grouped_df['y'] )
    grouped_df['x'], grouped_df['y'] = grouped_df['x'] * 4.5, grouped_df['y'] * 4.5
    grouped_df['z'] = grouped_df['z'] * 85.0
    return grouped_df
        
def neuron_vectors( neuron, scaled_df ):
    neuron_df = scaled_df[ scaled_df['post'].str.contains( neuron ) ].append( \
            scaled_df[ scaled_df['pre'].str.contains( neuron ) ] )[['z', 'pre', 'post', 'x', 'y', 'type', 'contin' ]]
    syn_types, coords, syn_id_lst, num_coords = [], [], [], []
    for synapse in neuron_df.values:
        if synapse[5] == 'electrical':
            if synapse[1] == neuron:
                syn_id_lst.append( synapse[2] ), syn_types.append( 'gap' )
            else:
                syn_id_lst.append( synapse[1] ), syn_types.append( 'gap' )
        elif synapse[1] == neuron:
            syn_id_lst.append( synapse[2] ), syn_types.append( 'post' )
        elif neuron in synapse[2]:
            syn_id_lst.append( synapse[1] ), syn_types.append( 'pre' )
        xyz = '(%s %s %s)' % ( synapse[3], synapse[4], synapse[0] )
        coords.append( xyz )
        num_coords.append( [ synapse[3], synapse[4], synapse[0] ] )
    print_vectors( neuron, syn_types, coords, syn_id_lst, '\t' )

def print_vectors( neuron, syn_types, coords, syn_id_lst, sep ):
    print '>%s' % ( neuron )
    print sep.join( syn_id_lst )
    print sep.join( syn_types )
    print sep.join( coords )
    
        
def graph_neuron( neuron, full_df, sec_dim ):
    neuron_df = full_df[ full_df['post'].str.contains( neuron ) ].append( \
            full_df[ full_df['pre'].str.contains( neuron ) ] )[['z', 'pre', 'post', 'x', 'y', 'type', 'contin' ]]
    z, pre_labels, post_labels, typ = neuron_df['z'].values, neuron_df['pre'].values, neuron_df['post'].values, neuron_df['type'].values
    if sec_dim.lower() == 'x':
        x = neuron_df['x'].values
    else:
        x = neuron_df['y'].values
    plt.figure()
    for i in range( len( pre_labels ) ):
        if typ[i] == 'electrical':
            plt.plot( z[i], x[i], 'co')
            if pre_labels[i] == neuron:
                plt.text( z[i], float(x[i]), post_labels[i], fontsize=4, alpha=0.6)
            else:
                plt.text( z[i], float(x[i]), pre_labels[i], fontsize=4, alpha=0.6)
        elif pre_labels[i] == neuron:
            plt.plot( z[i], x[i], 'ro')
            plt.text( z[i], float(x[i]), post_labels[i], fontsize=4, alpha=0.6)
        else:
            plt.plot( z[i], x[i], 'mo')
            plt.text( z[i], float(x[i]), pre_labels[i], fontsize=4, alpha=0.6)
    plt.title( neuron ), plt.xlabel( 'z (nm)' ), plt.ylabel( sec_dim + ' (nm)')
    plt.savefig( neuron + sec_dim + '.png' )
    plt.show()
    plt.close()

def main():
    # [ pre, post, type, continNum ]
    syn = pd.DataFrame( read_in_data( 'synapsecombined', [1,2,3,19] ),\
            columns=['pre', 'post', 'type', 'contin'] )
    obj = pd.DataFrame( read_in_data( 'object', [1,2,4,5] ), \
            columns=['x', 'y', 'img_num', 'contin'] )
    full_df = get_section( pd.merge( syn, obj, on='contin') )
    grouped_df = group_contins( full_df )
    scaled_df = scale_xyz( grouped_df )
    all_neurons = set( grouped_df['pre'].values )
    for neuron in all_neurons:
        neuron_vectors( neuron, scaled_df )
    if sys.argv[2].lower() == 'none':
        pass
    else:
        graph_neuron( sys.argv[2], scaled_df, sys.argv[3] )

main()
