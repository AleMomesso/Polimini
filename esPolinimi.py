from itertools import imap, imap, groupby, chain, imap
from operator import itemgetter
from sys import argv
from array import array
import matplotlib.pyplot as plt
import numpy as np
import time

 
def concat_map(func, it):
    return list(chain.from_iterable(imap(func, it)))
 
def minima(poly):
    """trova le coordinate minime di un polimino"""
    return (min(pt[0] for pt in poly), min(pt[1] for pt in poly))
 
def translate_to_origin(poly):
    (minx, miny) = minima(poly)
    return [(x - minx, y - miny) for (x, y) in poly]
 
rotate90   = lambda (x, y): ( y, -x)
rotate180  = lambda (x, y): (-x, -y)
rotate270  = lambda (x, y): (-y,  x)
reflect    = lambda (x, y): (-x,  y)
 
def rotations_and_reflections(poly):
    """tutte le simmetrie"""
    return (poly,
            map(rotate90, poly),
            map(rotate180, poly),
            map(rotate270, poly),
            map(reflect, poly),
            [reflect(rotate90(pt)) for pt in poly],
            [reflect(rotate180(pt)) for pt in poly],
            [reflect(rotate270(pt)) for pt in poly])
 
def canonical(poly):
    return min(sorted(translate_to_origin(pl)) for pl in rotations_and_reflections(poly))
 
def unique(lst):
    lst.sort()
    return map(next, imap(itemgetter(1), groupby(lst)))
 
contiguous = lambda (x, y): [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
 
def new_points(poly):
    """Trova tutti i punti unici che possono essere aggiunti al polimino"""
    return unique([pt for pt in concat_map(contiguous, poly) if pt not in poly])
 
def new_polys(poly):
    return unique([canonical(poly + [pt]) for pt in new_points(poly)])
 
monomino = [(0, 0)]
monominoes = [monomino]
 
def rank(n):
    """Genera in maniera ricorsiva polimini di categoria N"""
    assert n >= 0
    if n == 0: return []
    if n == 1: return monominoes
    return unique(concat_map(new_polys, rank(n - 1)))

def text_representation(poly,n):
     """Rappresentazione testuale"""
    min_pt = minima(poly)
    max_pt = (max(p[0] for p in poly), max(p[1] for p in poly))
    table = [[ 0 for i in xrange(n) ] for j in xrange(n)]
    for pt in poly:
        table[pt[0] - min_pt[0]][pt[1] - min_pt[1]] = 1
    return table
 
def main():
    
    n=input("Inserisci N: ")
    print ["Totale numeri polinomi:" ,len(rank(n))]
    
    j=1

    w=10
    h=10
    fig=plt.figure(figsize=(8, 8))
    columns = 5
    rows = (len(rank(n))/columns)+1    
    fig.suptitle('Tutti i polinomi con: ' + str(n) + ' quadrati')
    fig.patch.set_visible(False)
    plt.axis('off')

    
    for poly in rank(n):              
        s = text_representation(poly,n)  
        fig.add_subplot(rows, columns, j)
        fig.patch.set_visible(False)
        plt.axis('off')
        plt.imshow(s)
        j+=1       
   
    plt.show()
 
main()

