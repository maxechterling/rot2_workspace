#!/usr/bin/env python

import numpy as np
import math

high_scoring = [ 3000, 2000, 3500 ]
low_scoring = [ 13000, 12000, 13400 ]
high_scoring2 = [ 3000, 2000, 3500, 3000, 2000, 3500 ]
low_scoring2 = [ 13000, 12000, 13400, 13000, 12000, 13400 ]

## ordered scores
# high_scoringA = [ 3000, 2000, 3500, 3000, 2000, 3500 ]
# high_scoringB = [ 3000, 2000, 3500 ]
# high_scoringC = [ 3000, 2000 ]
# low_scoringA = [ 13000, 12000, 13400, 13000, 12000, 13400 ]
# low_scoringB = [ 13000, 12000, 13400 ]
# low_scoringC = [ 13000, 12000 ]

def method1( scores ):
    invert = [ ( 1. / x ) for x in scores ]
    return np.log( sum( invert ) )

def method2( scores ):
    return len( scores ) / np.log( sum( scores ) )
    
def method3( scores ):
    return 1. / np.log( (  sum( scores ) ) / len( scores ) )
    
def method4( scores ):
    return len( scores ) / np.log( (  sum( scores ) ) / len( scores ) )

def eval( method ):
    print 'few_clustered'
    print method( high_scoring )
    print '\nfew_disbursed'
    print method( low_scoring )
    print '\nmany_clustered'
    print method( high_scoring2 )
    print '\nmany_disbursed'
    print method( low_scoring2 )
    
eval( method2 )