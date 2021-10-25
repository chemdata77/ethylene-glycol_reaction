from ase.db import connect
from ase import Atoms
from ase.visualize import view
from ase.formula import Formula


db = connect("/data/qzh/qm9.db")
rows = list(db.select(sort='id')) 
for row in rows:
    #print(type(row.toatoms().symbols))
    atoms = row.toatoms()
    if (str(atoms.symbols) == Formula('C2H6O2')):
        print('row.id',row.id)
    

