from itertools import imap, imap, groupby, chain, imap
from operator import itemgetter
from sys import argv
from array import array
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time

 
def concat_map(func, it):
    return list(chain.from_iterable(imap(func, it)))
 
def minima(poly):
    """trova le coordinate(x,y) minime di un polimino"""
    return (min(pt[0] for pt in poly), min(pt[1] for pt in poly))
 
def translate_to_origin(poly):
    (minx, miny) = minima(poly)
    return [(x - minx, y - miny) for (x, y) in poly]
 
rotate90   = lambda (x, y): ( y, -x)
rotate180  = lambda (x, y): (-x, -y)
rotate270  = lambda (x, y): (-y,  x)
reflect    = lambda (x, y): (-x,  y)
 
def rotations_and_reflections(poly):
    """tutte le simmetrie piane"""
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
   
def cli_debug(poly):
    """polimini testuali per debug CLI"""
    min_pt = minima(poly)
    max_pt = (max(p[0] for p in poly), max(p[1] for p in poly))
    table = [array('c', ' ') * (max_pt[1] - min_pt[1] + 1)
             for _ in xrange(max_pt[0] - min_pt[0] + 1)]
    for pt in poly:
        table[pt[0] - min_pt[0]][pt[1] - min_pt[1]] = '#'
    return "\n".join(row.tostring() for row in table)
   
def poly_matrix_builder(poly,n):
    """Costruzione della matrice del polimino"""
    min_pt = minima(poly)
    max_pt = (max(p[0] for p in poly), max(p[1] for p in poly))
    table = [[ 0 for i in xrange(n) ] for j in xrange(n)]
    for pt in poly:
        table[pt[0] - min_pt[0]][pt[1] - min_pt[1]] = 1
    return table
 
def main():
    
    n=input("Inserisci N quadrati: ")           #lettura input di n quadrati
    lista_polimini = rank(n)                    #genero i vari polimini univoci
    conta_polimini = len(rank(n))               #conto il totale dei polimini univoci
    print ["Totale numeri polimini:" ,conta_polimini]
    
    colors = ['white', 'green', 'orange', 'blue', 'yellow', 'purple']    #lista colori per parte grafica
    bounds = [0,1,2,3,4,5,6]                                             #serve sempre per la gestione dei colori

    cmap = mpl.colors.ListedColormap(colors)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    fig=plt.figure(figsize=(8, 8))              #imposto la dimensione di ogni polimino generato
    columns = 5                                 #voglio disegnare 5 polimini per riga
    rows = (conta_polimini/columns)+1           #calcolo dinamico per ottenere il numero di righe necessarie per ospitare tutti i vari polimini
    fig.suptitle('Tutti i polimini con: ' + str(n) + ' quadrati' + ' (' + str(conta_polimini)+')')      #imposto titolo al foglio grafico
    
    j=1                                         #contatore che servirà in seguito per il ciclo for

    for poly in lista_polimini:    
        print cli_debug(poly), "\n"             #stampo su console i polimini in maniera testuale
        s = poly_matrix_builder(poly,n)         #costruisco una matrice con il polimino generato
        fig.add_subplot(rows, columns, j)       #imposto il punto in cui verrà inserito il polimino sul foglio grafico       
        fig.patch.set_visible(False)            #rimuovo il frame dal foglio grafico generato dalla matrice
        plt.axis('off')                         #rimuovo gli assi dal foglio grafico generato dalla matrice
        plt.imshow(s, interpolation='none', cmap=cmap, norm=norm)   #aggiungo il polimino generato alla parte grafica
        j+=1       
    #Stampa dei polimini
    plt.show()                                  #stampo il foglio grafico generato
 
main()
