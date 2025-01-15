# Lets Throw Some Tech At A Cappella

Everyone who's anyone in a cappella has done the `1`, `1,2,1`, `1,2,3,2,1`... round in warmups. **Let's throw some tech at it.**

## Background Info
For all you NARPS (Non-A cappella Regular People) out there, this warmup is one of the harder ones. You start singing scales like `1`, `1,2,1`, `1,2,3,2,1`... until you get to `1,2,...,8,...2,1` (there are 8 notes in an octatonic scale). Then you do it in reverse, starting at `8` and stopping once you've sang `8,7,...,1,...7,8`. Next you split up into groups and sing the scales in a round. So group one goes "`1`, `1,2,1`", and right on that last `1`, group two comes in with their own "`1`, `1,2,1`...", so on and so forth.

However, nobody's truly mastered the art of a cappella until you can pause on any given set of numbers through the round. For example, omitting the number `3` would sound like this: `1`, `1,2,1`, `1,2,_,2,1`, `1,2,_,4,_2,1`...

And this raises some interesting questions...

## Rationale
Given that groups are omitting the same numbers in the round, would it ever be possible for every group to pause in unison?

And let's take it even a bit further...

What's the maximum mutual pauses we could get? Which numbers should we omit? With 2 groups? With 3 groups? With everyone singing alone?

The Sings currently have 25 members... let's figure it out!

## Pretty Graph
In the graph below, we can see the interesting trends in the data. Wow, so cool!

<img src="https://github.com/raphaelpreston/1121/blob/master/1121graph.png" width=1500>

## The Code
```python
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

# returns a list where the ith entry is a list of indices of pauses for group i
def getBlanks( start, end, omits, numGroup ):
    totals = [ '*' for _ in range( 3 * numGroup ) ] # wait for their turn
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
    m = max(map(max, blanks)) # max number of pauses
    # check if any blanks are shared
    shared = []
    for i in range( 0, m + 1 ): # every possible index to pause on
        if inAll( i, blanks ):
            shared.append( i )
    return shared

# Runner
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
```

## Interesting Observations

* No matter the number of groups, the max number of pauses always occurs if we omit all numbers from `1-8` (duh).
* The number of mutual pauses decreases as we add groups (duh).
* The only way to get any mutual pauses while omitting exactly one number is to sing the round in two groups and omit the number `2`. This gives you six total pauses.
* With seven or more groups, it's impossible to pause together if you omit only two numbers. But for fewer than seven groups, you'll always get the most pauses if you omit `2` and `5`.
* When omitting five numbers, you'll always be able to get at least one mutual pause unless everyone is singing on their own (25 groups).
* As we omit more/fewer numbers, there's a seemingly unpredictable number of different combinations that always yield the max number of mutual pauses for the different amounts of groups. When we omit seven numbers, for all the different numbers of groups, there are only `2` different combinations of omitted numbers that always yield the max number of mutual pauses. For six numbers, there are `5`, for five there are `2`, for for four there are `3`, for three there are `2` and for one there is `1`. What the heck kind of pattern is that??

## Conclusion
We realistically never split up into more than three groups or omit more than two numbers. So, to achieve the bliss of perfectly synchronized pauses, we have a couple options. If we split into two groups, we can get `6` pauses if we omit the number `2`, and `18` pauses if we omit `2` and `5`. In three groups, we only have one option: get `9` pauses by omitting `2` and `5`.

Therefore, for the best ROI, we should split into two groups and omit the numbers `2` and `5`, yielding a total of `18` moments of euphoric silence.


## Full Results
|Groups|# of Numbers Omitted|Max # of Pauses|Which Numbers Omitted?|
|---|---|---|---|
|2|1|6|2|
|2|2|18|2, 5|
|2|3|33|1, 4, 7|
|2|4|48|1, 3, 4, 7|
|2|5|65|2, 3, 5, 6, 8|
|2|6|80|1, 2, 3, 5, 6, 8|
|2|7|100|1, 2, 3, 4, 5, 6, 8|
|2|8|125|1, 2, 3, 4, 5, 6, 7, 8|
|3|1|0|None|
|3|2|9|2, 5|
|3|3|19|1, 4, 7|
|3|4|36|1, 3, 4, 7|
|3|5|53|2, 3, 5, 6, 8|
|3|6|66|1, 2, 3, 5, 6, 8|
|3|7|89|1, 2, 3, 4, 5, 6, 8|
|3|8|122|1, 2, 3, 4, 5, 6, 7, 8|
|4|1|0|None|
|4|2|5|2, 5|
|4|3|12|1, 4, 7|
|4|4|27|1, 3, 4, 7|
|4|5|44|2, 3, 5, 6, 8|
|4|6|57|1, 3, 4, 6, 7, 8|
|4|7|82|1, 3, 4, 5, 6, 7, 8|
|4|8|119|1, 2, 3, 4, 5, 6, 7, 8|
|5|1|0|None|
|5|2|2|2, 5|
|5|3|8|1, 3, 4|
|5|4|20|2, 5, 6, 8|
|5|5|37|2, 3, 5, 6, 8|
|5|6|49|1, 3, 4, 6, 7, 8|
|5|7|76|1, 3, 4, 5, 6, 7, 8|
|5|8|116|1, 2, 3, 4, 5, 6, 7, 8|
|6|1|0|None|
|6|2|1|2, 5|
|6|3|6|1, 3, 4|
|6|4|14|2, 5, 6, 8|
|6|5|31|2, 3, 5, 6, 8|
|6|6|42|1, 3, 4, 6, 7, 8|
|6|7|71|1, 3, 4, 5, 6, 7, 8|
|6|8|113|1, 2, 3, 4, 5, 6, 7, 8|
|7|1|0|None|
|7|2|0|None|
|7|3|4|1, 3, 4|
|7|4|10|3, 5, 6, 8|
|7|5|25|2, 3, 5, 6, 8|
|7|6|36|1, 3, 4, 6, 7, 8|
|7|7|66|1, 3, 4, 5, 6, 7, 8|
|7|8|110|1, 2, 3, 4, 5, 6, 7, 8|
|8|1|0|None|
|8|2|0|None|
|8|3|3|1, 3, 4|
|8|4|9|3, 5, 6, 8|
|8|5|21|2, 3, 5, 6, 8|
|8|6|33|3, 4, 5, 6, 7, 8|
|8|7|62|1, 3, 4, 5, 6, 7, 8|
|8|8|107|1, 2, 3, 4, 5, 6, 7, 8|
|9|1|0|None|
|9|2|0|None|
|9|3|2|1, 3, 4|
|9|4|8|3, 5, 6, 8|
|9|5|19|2, 3, 5, 6, 8|
|9|6|30|3, 4, 5, 6, 7, 8|
|9|7|59|1, 3, 4, 5, 6, 7, 8|
|9|8|104|1, 2, 3, 4, 5, 6, 7, 8|
|10|1|0|None|
|10|2|0|None|
|10|3|1|1, 3, 4|
|10|4|7|3, 5, 6, 8|
|10|5|17|2, 3, 5, 6, 8|
|10|6|27|3, 4, 5, 6, 7, 8|
|10|7|56|1, 3, 4, 5, 6, 7, 8|
|10|8|101|1, 2, 3, 4, 5, 6, 7, 8|
|11|1|0|None|
|11|2|0|None|
|11|3|0|None|
|11|4|6|3, 5, 6, 8|
|11|5|15|2, 3, 5, 6, 8|
|11|6|24|2, 3, 5, 6, 7, 8|
|11|7|53|1, 3, 4, 5, 6, 7, 8|
|11|8|98|1, 2, 3, 4, 5, 6, 7, 8|
|12|1|0|None|
|12|2|0|None|
|12|3|0|None|
|12|4|5|3, 5, 6, 8|
|12|5|13|1, 3, 4, 6, 7|
|12|6|22|2, 3, 5, 6, 7, 8|
|12|7|50|1, 3, 4, 5, 6, 7, 8|
|12|8|95|1, 2, 3, 4, 5, 6, 7, 8|
|13|1|0|None|
|13|2|0|None|
|13|3|0|None|
|13|4|4|3, 5, 6, 8|
|13|5|12|1, 3, 4, 6, 7|
|13|6|20|1, 3, 4, 6, 7, 8|
|13|7|47|1, 3, 4, 5, 6, 7, 8|
|13|8|92|1, 2, 3, 4, 5, 6, 7, 8|
|14|1|0|None|
|14|2|0|None|
|14|3|0|None|
|14|4|3|3, 5, 6, 8|
|14|5|11|1, 3, 4, 6, 7|
|14|6|19|1, 3, 4, 6, 7, 8|
|14|7|44|1, 3, 4, 5, 6, 7, 8|
|14|8|89|1, 2, 3, 4, 5, 6, 7, 8|
|15|1|0|None|
|15|2|0|None|
|15|3|0|None|
|15|4|2|3, 5, 6, 8|
|15|5|10|1, 3, 4, 6, 7|
|15|6|18|1, 3, 4, 6, 7, 8|
|15|7|41|1, 3, 4, 5, 6, 7, 8|
|15|8|86|1, 2, 3, 4, 5, 6, 7, 8|
|16|1|0|None|
|16|2|0|None|
|16|3|0|None|
|16|4|1|3, 5, 6, 8|
|16|5|9|1, 3, 4, 6, 7|
|16|6|17|1, 3, 4, 6, 7, 8|
|16|7|38|1, 3, 4, 5, 6, 7, 8|
|16|8|83|1, 2, 3, 4, 5, 6, 7, 8|
|17|1|0|None|
|17|2|0|None|
|17|3|0|None|
|17|4|0|None|
|17|5|8|1, 3, 4, 6, 7|
|17|6|16|1, 3, 4, 6, 7, 8|
|17|7|35|1, 3, 4, 5, 6, 7, 8|
|17|8|80|1, 2, 3, 4, 5, 6, 7, 8|
|18|1|0|None|
|18|2|0|None|
|18|3|0|None|
|18|4|0|None|
|18|5|7|1, 3, 4, 6, 7|
|18|6|15|1, 3, 4, 6, 7, 8|
|18|7|32|1, 3, 4, 5, 6, 7, 8|
|18|8|77|1, 2, 3, 4, 5, 6, 7, 8|
|19|1|0|None|
|19|2|0|None|
|19|3|0|None|
|19|4|0|None|
|19|5|6|1, 3, 4, 6, 7|
|19|6|14|1, 3, 4, 6, 7, 8|
|19|7|29|1, 3, 4, 5, 6, 7, 8|
|19|8|74|1, 2, 3, 4, 5, 6, 7, 8|
|20|1|0|None|
|20|2|0|None|
|20|3|0|None|
|20|4|0|None|
|20|5|5|1, 3, 4, 6, 7|
|20|6|13|1, 3, 4, 6, 7, 8|
|20|7|27|1, 3, 4, 5, 6, 7, 8|
|20|8|71|1, 2, 3, 4, 5, 6, 7, 8|
|21|1|0|None|
|21|2|0|None|
|21|3|0|None|
|21|4|0|None|
|21|5|4|1, 3, 4, 6, 7|
|21|6|12|1, 3, 4, 6, 7, 8|
|21|7|25|1, 3, 4, 5, 6, 7, 8|
|21|8|68|1, 2, 3, 4, 5, 6, 7, 8|
|22|1|0|None|
|22|2|0|None|
|22|3|0|None|
|22|4|0|None|
|22|5|3|1, 3, 4, 6, 7|
|22|6|11|1, 3, 4, 6, 7, 8|
|22|7|23|1, 3, 4, 5, 6, 7, 8|
|22|8|65|1, 2, 3, 4, 5, 6, 7, 8|
|23|1|0|None|
|23|2|0|None|
|23|3|0|None|
|23|4|0|None|
|23|5|2|1, 3, 4, 6, 7|
|23|6|10|1, 3, 4, 6, 7, 8|
|23|7|21|1, 3, 4, 5, 6, 7, 8|
|23|8|62|1, 2, 3, 4, 5, 6, 7, 8|
|24|1|0|None|
|24|2|0|None|
|24|3|0|None|
|24|4|0|None|
|24|5|1|1, 3, 4, 6, 7|
|24|6|9|1, 3, 4, 6, 7, 8|
|24|7|20|1, 3, 4, 5, 6, 7, 8|
|24|8|59|1, 2, 3, 4, 5, 6, 7, 8|
|25|1|0|None|
|25|2|0|None|
|25|3|0|None|
|25|4|0|None|
|25|5|0|None|
|25|6|8|1, 3, 4, 6, 7, 8|
|25|7|19|1, 3, 4, 5, 6, 7, 8|
|25|8|56|1, 2, 3, 4, 5, 6, 7, 8|

---
*Raphael Preston*
