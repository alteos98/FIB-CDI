
'''
Dada una ddp p, hallar su entropía.
'''
def H1(p):
    sum = 0.0
    for x in p:
        if x != 0:
            sum += x * math.log2(x)
    return -sum