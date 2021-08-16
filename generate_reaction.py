# -*- coding: utf-8 -*

from __future__ import absolute_import, division, print_function, unicode_literals
# import tensorflow as tf
# from tensorflow import keras
import multiprocessing
import os
import numpy as np
import matplotlib.pyplot as plt
from progress.bar import Bar
# logging.info(tf.__version__)
from scipy.optimize import minimize
from itertools import combinations
from ase.visualize import view
from ase.db import connect
import random
from ase.build import sort
from ase import Atom
from ase.visualize import view   
from ase.io import read, write
from base64 import b64encode, b64decode
import itertools
import logging

logging.info('git commit id is: ' + str(os.popen('git --no-pager log -1 --oneline').read()))

seed = 1234
random.seed(seed)
np.random.seed(seed)
logging.info('random.seed: '+str(seed))
multi_thd = False 

# properties
A = "rotational_constant_A"
B = "rotational_constant_B"
C = "rotational_constant_C"
mu = "dipole_moment"
alpha = "isotropic_polarizability"
homo = "homo"
lumo = "lumo"
gap = "gap"
r2 = "electronic_spatial_extent"
zpve = "zpve"
U0 = "energy_U0"
U = "energy_U"
H = "enthalpy_H"
G = "free_energy"
Cv = "heat_capacity"

db = connect('./qm9.db')
# 16.1% memory usage of a 128G machine
rows = list(db.select(sort='id'))
# rows = list(db.select('id<200'))

atom_names = ['H', 'C', 'O', 'F', 'N']
atom_dict = {'H': 0, 'C':1, 'O':2, 'F':3, 'N':4}
atom_cnt_lst = []
atom_cnt_dict = {}

unit = 1

def get_data_pp(idx, type):
    # extract properties
    prop = 'None'
    # row = db.get(id=idx)
    row = rows[idx-1]
    if(row.id != idx):
        1/0
    # extract from schnetpack source code
    shape = row.data["_shape_" + type]
    dtype = row.data["_dtype_" + type]
    prop = np.frombuffer(b64decode(row.data[type]), dtype=dtype)
    prop = prop.reshape(shape)
    return prop

def hash_1d_array(arr):
    ret = 0
    arr = list(arr)
    for i in range(len(arr)):
        ret += (arr[i] * pow(50, (len(arr) - i)))
    return ret

def multi_thd_reac(reac_lst_orig,xishu):
    ret = reac_lst_orig
    k=xishu[0]
    p=xishu[1]
    q=xishu[2]
    g1 = get_data_pp(idx=reac_lst_orig[0], type=G)[0] * unit
    g2 = get_data_pp(idx=reac_lst_orig[1], type=G)[0] * unit
    g3 = get_data_pp(idx=reac_lst_orig[2], type=G)[0] * unit
    homo1 = get_data_pp(idx=reac_lst_orig[0], type=homo)[0]
    homo2 = get_data_pp(idx=reac_lst_orig[1], type=homo)[0]
    homo3 = get_data_pp(idx=reac_lst_orig[2], type=homo)[0]
    lumo1 = get_data_pp(idx=reac_lst_orig[0], type=lumo)[0]
    lumo2 = get_data_pp(idx=reac_lst_orig[1], type=lumo)[0]
    lumo3 = get_data_pp(idx=reac_lst_orig[2], type=lumo)[0]
    
    judgment_mode = 3 # 0: G; 1: homo-lumo;  3: G + homo-lumo
    lumo_r, homo_r = 0, 0
    if(judgment_mode == 0):
        if(g1*k+g2*p-g3*q>0): # A + B => C
            ret.append(1)
        else:
            ret.append(-1) # C => A + B
        ret.append([g1,k,g2,p,g3,q,g3*q-g1*k-g2*p])
    elif(judgment_mode == 1):
        if(abs(lumo2-homo1) < abs(lumo1-homo2)):
            lumo_r = lumo2
            homo_r = homo1
        else:
            lumo_r = lumo1
            homo_r = homo2
        if(lumo3 > lumo_r and homo3 < homo_r):
            ret.append(1) # A + B => C
        else:
            ret.append(-1) # C => A + B
        ret.append([homo1,lumo1,homo2,lumo2,homo3,lumo3])
    
    elif(judgment_mode == 3):
        if(abs(lumo2-homo1) < abs(lumo1-homo2)):
            lumo_r = lumo2
            homo_r = homo1
        else:
            lumo_r = lumo1
            homo_r = homo2
        if((lumo3 > lumo_r and homo3 < homo_r) and (g1*k+g2*p-g3*q>0)): # A + B => C
            ret.append(1)
        else:
            ret.append(-1) # C => A + B
    else:
        pass
    return ret

if __name__ == '__main__':
    for row in rows:
        at = row.toatoms()
        atom_cnt = [0] * len(atom_names)
        for a in at:
            atom_cnt[atom_dict[a.symbol]] += 1
        atom_cnt_lst.append(np.array(atom_cnt))
        if row.id == 42:
           k1 = hash_1d_array(np.array(atom_cnt)) 
        k = hash_1d_array(np.array(atom_cnt))
        if(atom_cnt_dict.__contains__(k)):
            atom_cnt_dict[k].append(row.id)
        else:
            atom_cnt_dict[k] = [row.id]
    # print(len(atom_cnt_lst))
    # print(len(atom_cnt_dict))
    dk = list(atom_cnt_dict.keys())
    reac_cnt = 0
    reac_lst = []
    xishu = []
    temp = []

    for i in range(len(dk)):     
        for j in range(i, len(dk)):
            for k in range(1,6):
                for p in range(1,6):
                    for q in range(1,6):
                        #if(atom_cnt_dict.__contains__(dk[i]*k+dk[j]*p)):
                        if(atom_cnt_dict.__contains__(dk[i]*k+k1*p)):
                            #if dk[i]*k+dk[j]*p == k1*q:
                            if dk[i]*k+k1*p == dk[j]*q:
                                #reac_cnt += (len(atom_cnt_dict[dk[i]]) * len(atom_cnt_dict[dk[j]]) * len(atom_cnt_dict[k1]))
                                reac_cnt += (len(atom_cnt_dict[dk[i]]) * len(atom_cnt_dict[k1]) * len(atom_cnt_dict[dk[j]]))

                                #print(atom_cnt_dict[(dk[i]+dk[j])][0])

                                #s = [atom_cnt_dict[dk[i]], atom_cnt_dict[dk[j]], atom_cnt_dict[k1]]         
                                s = [atom_cnt_dict[dk[i]], atom_cnt_dict[k1], atom_cnt_dict[dk[j]]]
                 
                                xishu = [k,p,q]
                                
                                reac_lst_idx = []
                                reac_lst_idx += list(itertools.product(*s)) 
                                #reac_lst_idx.append(xishu)
                                reac_lst_res = []
                                reac_lst_res.extend((reac_lst_idx, xishu))
                                reac_lst.append(reac_lst_res)
                                #print('qqq',reac_lst)
    for i in range(len(reac_lst)):
        for j in range(len(reac_lst[i])-1):
            for k in range(len(reac_lst[i][j])):
                reac_lst[i][j][k] = list(reac_lst[i][j][k])
        
    reac_lst_1 = []

    for m in range(len(reac_lst)):
        if(multi_thd):
            pool = multiprocessing.Pool(2)
            reac_lst_1 = pool.map(multi_thd_reac, reac_lst[m][0],reac_lst[m][1])
            temp = reac_lst_1
        else:
            for z in reac_lst[m][0]:
                reac_lst_1.append(multi_thd_reac(z,reac_lst[m][1]))
            temp = reac_lst_1
    import pickle
    #with open('Product_reactions_all_test_81.txt', 'wb') as fp:
    with open('Reactant_reactions_all_test_81.txt', 'wb') as fp:

        pickle.dump(temp, fp)

