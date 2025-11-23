import pandas as pd
import numpy as np 
from .functions import *
import hashlib
import random

def generate_BAH_dataset(xsf_dir,divs,ncpu):
    """
    Generates a dataset of BAH selected files from XSF files in the BAH_structures directory.

    Args:
        xsf_directory (str): Path to the directory containing XSF files.
        divs: number of bins.
        threads: no. of cores for multiprocessing.

    """
    import os
    xsf_directory = xsf_dir
    xsf_files = [f for f in os.listdir(xsf_directory) if f.endswith(".xsf")]

    data=[]
    for file_name in xsf_files:
    # Read the .xsf file
         atoms, coords, gradients, total_energy = read_xsf(os.path.join(xsf_directory, file_name))
         natoms=len(atoms)
         CM=get_CM(natoms,atoms,coords)
         reshape_CM=(CM.reshape(-1))
         row = [file_name] + reshape_CM.tolist()
         data.append(row)
    df = pd.DataFrame(data)


    coord_indx=df.iloc[:,0]
    coord_indx

    X=df.iloc[0:,1:]
    Y=pd.DataFrame(np.zeros((X.shape[0],X.shape[1])))

    Y = parallel_process(X, divs,threads=ncpu)
#    print(Y)



    hash_table={}

    for entry in range(X.shape[0]):
         bin_string=Y.iloc[entry].astype(str).to_string(index=False).replace('\n','').replace(' ', '')
         hash_value=hashlib.sha256(bin_string.encode())
         hash_value=str(hash_value.hexdigest())
         hash_table.setdefault(hash_value,[])
         hash_table[hash_value].append(entry)
    

    with open("hashtable.txt", 'w') as f:    # save entire hash_table
       for key, value in hash_table.items():
           f.write('%s  :  %s\n' % (key, value))

    import shutil
    random_indx=[]
    with open("random_str.txt", 'w') as f:   # take out one structure randomly from each bin
         for key,value in hash_table.items():
             value=random.choice(value)
             random_index=random_indx.append(value)
             f.write('%s\n' % (value))

    
    selected_dir = "./BAH_selected"
    os.makedirs(selected_dir, exist_ok=True)

    # Copy selected files to BAH_selected directory
    for idx in random_indx:
        filename = takeout_coordindex(df,idx)
        src_path = os.path.join(xsf_directory, filename)
        dst_path = os.path.join(selected_dir, filename)
        shutil.copy(src_path, dst_path)
    print('###########################################################################################')
    print('BAH algorithm done.\nSelected structure xsf files are copied in BAH_structures')
    print('###########################################################################################')
    return hash_table,random_index,str(selected_dir)

#hash_table,random_index,selected_dir = generate_BAH_dataset(xsf_dir=xsf_directory)
