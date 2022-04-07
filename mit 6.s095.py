# mit 6.s095

#puzzle input
#Programming for the Puzzled 
#You Will All Conform
#Input is a vector of F's and B's, in terms of forwards and backwards caps
#Output is a set of commands (printed out) to get either all F's or all B's
#Fewest commands are the goal

caps = ['F', 'F', 'B', 'B', 'B', 'F', 'B', 'B', 'B', 'F', 'F', 'F', 'F' ]

def plzConform(caps):
    # init

    sta = 0
    f = 0
    b = 0
    intervals = []

    #同向标记
    for i in range(1, len(caps)):
        if caps[sta] != caps[i]:
            intervals.append((sta, i-1, caps[sta]))
            
            if caps[sta] == 'F':
                f += 1
            else:
                b += 1
            sta = i

    intervals.append((sta, len(caps)-1, caps[sta]))
    if caps[sta] == 'F':
        f += 1
    else:
        b += 1

    if f < b:
        flip = 'F'
    else:
        flip = 'B'

    for i in intervals:
        if i[2] == flip:
            print('{} - {}flip {}'.format(i[0], i[1], flip))

if __name__ == '__main__':
    plzConform(caps)


