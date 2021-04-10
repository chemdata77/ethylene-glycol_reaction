import pickle

#with open('out_reactions_homolumo.txt', 'rb') as fp:
with open('Reactant_reactions_homolumo.txt', 'rb') as fp:  
    b = pickle.load(fp) 
    
#print(b)
print(len(b))
reac = []
reac1 = []
for i in range(len(b)):
    if b[i][3] == 1:
        reac.append(b[i]) 
    if b[i][3] == -1:
        reac1.append(b[i])

with open('Reactant_reactions_hl_yes.txt', 'wb') as fp:    
    pickle.dump(reac, fp)

with open('Reactant_reactions_hl_no.txt', 'wb') as fp:  
    pickle.dump(reac1, fp)  

with open('Reactant_reactions_hl_yes.txt', 'rb') as fp:  
    z = pickle.load(fp)
#print(z) 
print(len(z))


with open('Reactant_reactions_hl_no.txt', 'rb') as fp:   
    h = pickle.load(fp) 
#print(h) 
print(len(h))           
