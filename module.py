from __future__ import division
from sympy import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)
init_printing() # doctest: +SKIP
from fractions import Fraction
from IPython.display import display, Latex
import ipywidgets as widgets
import numpy as np
from ipywidgets import interact ,Layout

def gg(A):
    B=A.col_insert(A.shape[0],eye(A.shape[0]))
    #pprint(B)
    display(Latex(f'$A={latex(B[:,:n])}\quad I_{n}={latex(B[:,n:])}\quad b={latex(B[:,-1])} $'))
    print('===================================================')   
    for i in range(A.shape[0]):
        if B.row(i)[i]==0 or isinstance(B.row(i)[i],Mul) or isinstance(B.row(i)[i],Add) or isinstance(B.row(i)[i],Symbol):
        #if B.row(i)[i]==0:
            for k in range(i+1, len(A)):
                
                if B.row(k)[i] !=0 and not(isinstance(B.row(k)[i],Mul) or isinstance(B.row(k)[i],Add) or isinstance(B.row(k)[i],Symbol)):
                    B=B.elementary_row_op('n<->m',row1=k, row2=i)
                    print(' -------- Permutation L{} <--> L{} --------'.format(k+1,i+1))
                    display(Latex("$L_{} \leftrightarrow L_{}$".format(k+1,i+1)))
                    #print("L{} <--> L{} ".format(k+1,i+1))
                    display(Latex(f'${latex(B[:,:n])}\quad {latex(B[:,n:])}\quad {latex(B[:,-1])} $'))
                    break;
            else:
                if B.row(i)[i]==0:
                    print('La matrice n''est pas inversible')
                    return None
        else :
            print(' --------------- Pas de permutation ---------------')
        if B.row(i)[i]!=1:
            #print("L{} <-- ({})*L{}".format(i+1,simplify(1/B.row(i)[i]),i+1))
            display(Latex("$L_{} \leftarrow ({})L_{}$".format(i+1,latex(simplify(1/B.row(i)[i])),i+1)))
            simplify(B.zip_row_op(i, i, lambda v, u: simplify(1/B.row(i)[i]*u)));
            display(Latex(f'${latex(B[:,:n])}\quad {latex(B[:,n:])}\quad {latex(B[:,-1])} $'))   
        for j in range(A.shape[0]):
            if j!=i and (B.row(j)[i]!=0):
                #print("L{} <-- L{} +({})*L{}".format(j+1,j+1,simplify(-B.row(j)[i]/B.row(i)[i]),i+1))
                display(Latex("$L_{} \leftarrow L_{}+({})L_{}$".format(j+1,j+1,latex(simplify(-B.row(j)[i]/B.row(i)[i])),i+1)))
                simplify(B.zip_row_op(j, i, lambda v, u: simplify(v -B.row(j)[i]/B.row(i)[i] *u)));
                display(Latex(f'${latex(B[:,:n])}\quad {latex(B[:,n:])} \quad {latex(B[:,-1])}$'))                
        print('===================================================')
    return B[:,n:],B[:,-1]
def indices(n,m):
    L= ['a{}{}'.format(i,j) for i in range(1,n+1)  for j in range(1,m+1)]
    return {u[0]+1:u[1] for u in enumerate(L)}
def wid(n,m):
    items = [widgets.Text(
    value='0',
    placeholder='a',
    description=indices(n,m)[i],
    layout=Layout(width='75%', height='75%'),
    disabled=False
) for i in indices(n,m).keys()]
    return widgets.GridBox(items, layout=widgets.Layout(grid_template_columns="repeat({}, 200px)".format(m)))
