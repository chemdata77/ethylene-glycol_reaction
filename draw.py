import pickle
import rdkit
import csv
from ase.db import connect
from rdkit import Chem
from rdkit.Chem import  Draw
from rdkit.Chem.Draw.MolDrawing import MolDrawing, DrawingOptions
from ase.io import write
#db = connect('./qm9.db')
#rows = list(db.select(sort='id'))

import pandas as pd
data = pd.read_csv("QM9.csv")

print(data['SMILES1'][0])
check = []
with open('out_reactions_all.txt', 'rb') as fp:  
#with open('Reactant_reactions_all.txt', 'rb') as fp:
    b = pickle.load(fp)
#print(b[0]) 
for i in range(len(b)):
    for j in range(3):
        if b[i][j] not in check:
            smi = data['SMILES1'][b[i][j]-1]
            m = Chem.MolFromSmiles(smi)
            f = 'picture_out/' + str(b[i][j]) + '.png'
            #f = str(b[i][j]) + '.png'
            Draw.MolToFile(m, f)
            check.append(b[i][j])
print(len(check))

#r = Chem.MolFromPDBFile('slab0.pdb')  

#smi = Chem.MolToSmiles(r)
#print(smi)

#m = Chem.MolFromSmiles(smi)
#Draw.MolToFile(m, '000.png')



#r1 = [img, img, 0]
#r2 = []
#p1 = []
#r2.append(r1)
#t = ["1", "2", "3"]
#with open("reaction.csv",'a+',newline='', encoding='utf-8') as f:#numline是来控制空的行数的
#    writer=csv.writer(f)#这一步是创建一个csv的写入器
#    writer.writerow(t)#写入标签
#    writer.writerows(r2)#写入样本数据
#for row in rows:
    #write('slab.pdb', row)
    
    #print(type(row))
    
    #r = Chem.MolFromPDBFile('slab.pdb')  
    #smi = Chem.MolToSmiles(r)
    #print(smi)

#    at = row.toatoms()
#    write('slab.pdb', at)

#    r = Chem.MolFromPDBFile('slab.pdb')  
#    print(type(at))
    #break
    #if row.id == r1:        
    #r = Chem.MolFromPDBFile(row)
#    smi = Chem.MolToSmiles(r)
#    print(smi)
        #img = Draw.SDToImage(row, options=opts)
#    break

