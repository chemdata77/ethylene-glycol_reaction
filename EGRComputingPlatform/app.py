import os
from flask import Flask, render_template, send_from_directory, request, jsonify, Markup
import pandas as pd
import numpy as np
import json
from flask import request
#from dgl.data.utils import save_graphs
from flask_cors import CORS
from ase.visualize import view
from ase.db import connect
import pickle
from rdkit import Chem
from rdkit.Chem import AllChem
import random


app = Flask(__name__)
CORS(app, resources=r'/*')
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
current_work_dir = os.path.dirname(__file__)  # 当前文件所在的目录
print(basedir)
ALLOWED_EXTENSIONS = set(['traj'])  # 允许上传的文件后缀

with open('Reactant_reactions_gibbs.txt','rb') as fp:
    b = pickle.load(fp)
with open('Reactant_reactions_hl.txt','rb') as fp:
    hl = pickle.load(fp)

db = connect("./qm9.db")
data = pd.read_csv("./QM9.csv")

rows = list(db.select(sort='id'))


# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 主
#@app.route('/', methods=['GET', 'POST'])
#def upload_test():
#    # return render_template('user/homepage.html')
#    if request.method == 'GET':
#        return render_template('user/homepage.html', input_file='', res_text='')
#    else:
#        inputText = request.form.get("input_file")
#        resText = Markup(formatRes((inputText)))
#        return render_template('user/homepage.html', input_file=inputText, res_text=resText)

@app.route('/method1', methods=['POST'])
def return_table():
    item = json.loads(request.get_data(as_text=True))
    #print(item['text'])
    G = int(item['text'][2:])
    print(G)
    res = []
    res1 = []
    res2 = []
    temp2 = {}
    for i in range(2):
        #print(i)
        temp1={}
        temp1['分子式'] = trans_symbols(b[G][i])
        temp1['分子系数'] = b[G][4][i*2+1]
        temp1['Gibbs/eV'] = ('%.3f' % b[G][4][i*2])
        temp1['HOMO/eV'] = ('%.3f' % hl[G][4][i*2])
        temp1['LUMO/eV'] = ('%.3f' % hl[G][4][i*2+1])

        res1.append(temp1)
        print(res1)
    temp2['分子式'] = trans_symbols(b[G][2])
    temp2['分子系数'] = b[G][4][5]
    temp2['Gibbs/eV'] = ('%.3f' % b[G][4][4])
    temp2['HOMO/eV'] = ('%.3f' % hl[G][4][4])
    temp2['LUMO/eV'] = ('%.3f' % hl[G][4][5])
    res2.append(temp2)
    res.append(res1)
    res.append(res2)
    print(res)
    return {"tabledata":res}

@app.route('/method2', methods=['POST'])
def return_qm9():
    item = json.loads(request.get_data(as_text=True)) 
    print(item['text'],item['text2'])
    #interval = item['text'].split('-')
    left = int(item['text'])-1
    right = int(item['text2'])+int(item['text'])-1 
   
    res = []
    node = {}
    edge = {}
    link = []
    print('loop start')
    for i in range(left, right):
        node[str(b[i][0])] = [trans_symbols(b[i][0]),trans_xyz(b[i][0])]
        node[str(b[i][1])] = [trans_symbols(b[i][1]),trans_xyz(b[i][1])]
        node[str(b[i][2])] = [trans_symbols(b[i][2]),trans_xyz(b[i][2])]
        
        edge[str(b[i][0])+'-'+str(i)] = str(('%.3f' % b[i][4][0]))
        edge[str(b[i][1])+'-'+str(i)] = str(('%.3f' % b[i][4][2]))
        edge[str(b[i][2])+'-'+str(i)] = str(('%.3f' % b[i][4][4]))
        node['*G'+str(i)] = str(('%.3f' % b[i][4][6]))
        
        link.append([str(b[i][0]),edge[str(b[i][0])+'-'+str(i)],'*G'+str(i)])
        link.append([str(b[i][1]),edge[str(b[i][1])+'-'+str(i)],'*G'+str(i)])
        link.append(['*G'+str(i),edge[str(b[i][2])+'-'+str(i)],str(b[i][2])])
    
    print('loop end')
    res.append([node])
    res.append(link)
    #print(res) 
    return {"tabledata":res}

@app.route('/method3', methods=['POST'])
def return_rand():
    item = json.loads(request.get_data(as_text=True)) 
    print(item['text'],item['text2'])
    tmp = item['text']
    if int(tmp) == 0:
        randlist=random.sample(range(1,len(b)),int(item['text2']))
   
    res = []
    node = {}
    edge = {}
    link = []
    print('loop start')
    for i in randlist:
        node[str(b[i][0])] = [trans_symbols(b[i][0]),trans_xyz(b[i][0])]
        node[str(b[i][1])] = [trans_symbols(b[i][1]),trans_xyz(b[i][1])]
        node[str(b[i][2])] = [trans_symbols(b[i][2]),trans_xyz(b[i][2])]
        
        edge[str(b[i][0])+'-'+str(i)] = str(('%.3f' % b[i][4][0]))
        edge[str(b[i][1])+'-'+str(i)] = str(('%.3f' % b[i][4][2]))
        edge[str(b[i][2])+'-'+str(i)] = str(('%.3f' % b[i][4][4]))
        node['*G'+str(i)] = str(('%.3f' % b[i][4][6]))
        
        link.append([str(b[i][0]),edge[str(b[i][0])+'-'+str(i)],'*G'+str(i)])
        link.append([str(b[i][1]),edge[str(b[i][1])+'-'+str(i)],'*G'+str(i)])
        link.append(['*G'+str(i),edge[str(b[i][2])+'-'+str(i)],str(b[i][2])])
    
    print('loop end')
    res.append([node])
    res.append(link)
    print(res) 
    return {"tabledata":res}

def trans_symbols(atoms_id):
    return str(rows[atoms_id-1].toatoms().symbols)
    # for row in rows:
    #     atoms = row.toatoms()
    #     if row.id == id:
    #         return str(atoms.symbols)

def trans_xyz(row_id):
    # print(data['SMILES1'])
    smi = data['SMILES1'][row_id-1]
    patt = Chem.MolFromSmiles(smi)
    m3 = Chem.AddHs(patt)
    AllChem.EmbedMolecule(m3, randomSeed=0xf00d)
    s = Chem.MolToXYZBlock(m3)
    s_list = s.split(" ")
    res = ""
    for i in s_list:
        res += str(i)
        res += ' '
    return repr(res[:-2])


if __name__ == '__main__':
    # print(data)
    app.run(debug=True,host="0.0.0.0",port=8888)
