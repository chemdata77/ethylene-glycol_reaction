import pickle

with open('out_reactions_gibbs.txt', 'rb') as fp:  
#with open('Reactant_reactions_gibbs.txt', 'rb') as fp:

    b = pickle.load(fp) 
    
#print(b)
print(len(b))

with open('out_reactions_homolumo.txt', 'rb') as fp:
    q = pickle.load(fp)


for i in range(len(b)):
    for j in range(i, len(q)):
        if b[i][:3] == q[j][:3]:
            #q[j].append(b[i][3])
            b[i].append(q[i][3])
            if b[i][3] == 1 and q[j][3] == 1:
                b[j].append(1)
            else:
                b[j].append(-1)
      
with open('out_reactions_all.txt', 'wb') as fp: 
    pickle.dump(b, fp) 


with open('out_reactions_all.txt', 'rb') as fp:  
    z = pickle.load(fp) 
print(z)
print(len(z)) 


