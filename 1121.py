import itertools

# helper function returns True if num is in each list in arrOfArrs
def inAll( num, arrOfArrs ):
    for arr in arrOfArrs:
        l = False
        for i in arr:
            if i == num:
                l = True
        if not l:
            return False
    return True

# returns the full range of "start...end...start"
def fullRange( start, end ):
    mod = 1 if start < end else -1
    return ( list( range( start, end + mod, mod ) ) +
           list( range( end - mod, start - mod, -1 * mod ) ) )

# returns a list where the ith value is a list of indices of pauses for group i
def getBlanks( start, end, omits, numGroup ):

    totals = [ '*' for _ in range( 3 * numGroup ) ]
    for i in range( start, end + 1 ): # forward
        totals += [ '_' if num in omits
                    else num for num in fullRange( start, i ) ]

    for i in range( end, start - 1, -1 ): # backwards
        totals += [ '_' if num in omits
                    else num for num in fullRange( end, i ) ]

    blanks = []
    for i, num in enumerate( totals ):
        if num == '_':
            blanks.append( i )

    return blanks

# returns list of all mutual pauses when numGroups groups sing a round
# from start to end, omitting each number in omits
def getSameBlanks( start, end, omits, numGroups ):
    blanks = []
    for i in range( numGroups ):
        blanks.append( getBlanks( start, end, omits, i ) )
    
    # get max
    m = max(map(max, blanks))

    # check if any blanks are shared
    shared = []
    for i in range( 0, m + 1 ):
        if inAll( i, blanks ):
            shared.append( i )
    
    return shared


start = 1
end = 8

print( "|groups|# of numbers omitted|max # of pauses|which numbers|" )
print( "|---|---|---|---|" )
for numGroups in range( 2, 26 ):
    for r in range( start, end + 1 ):
        maxOmits = 0
        maxOmitsComb = None
        combs = list( itertools.combinations( range( start, end + 1 ), r ) )
        for comb in combs:
            numShared = len( getSameBlanks( start, end, set( comb ),
                             numGroups ) )
            if numShared > maxOmits:
                maxOmits = numShared
                maxOmitsComb = comb
        s = ( str( list( maxOmitsComb ) )[ 1: -1 ] if maxOmitsComb != None
            else None )
        print( "|{}|{}|{}|{}|".format( numGroups, r, maxOmits, s ) )







