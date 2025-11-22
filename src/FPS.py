#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np 
import pandas as pd
from .functions import *
from skmatter.sample_selection import FPS # type: ignore
import numpy as np

#Please write the path where .xsf files are located and number of FPS structures to be selected.
xsf_directory = "/home/akash/work/VSCODE/BAH_FPS/BAH_FPS_CODE/test/testset"
FPS_structures=50


def furthest_point_sampling(xsf_dir, FPS_structures):
     xsf_directory = xsf_dir
     xsf_files = [f for f in os.listdir(xsf_directory) if f.endswith(".xsf")]

     data=[]
     for file_name in xsf_files:
         # Read the .xsf file
         atoms, coords, gradients, total_energy = read_xsf(os.path.join(xsf_directory, file_name))
         natoms = len(atoms)
         CM = get_CM(natoms, atoms, coords)
         reshape_CM = (CM.reshape(-1))
         row = [file_name] + reshape_CM.tolist()
         data.append(row)
#    print(file_name,'done')
     df = pd.DataFrame(data)
     df.to_csv('data_CM.csv', index=False)


     df = pd.read_csv('data_CM.csv')
     all_CM=df.iloc[0:,1:]

     selector = FPS(n_to_select=FPS_structures,
     initialize='random',)
     X = all_CM
     selector.fit(X)
     selected_index = selector.selected_idx_

     import numpy as np
     import shutil
     np.set_printoptions(suppress=True)
     selected_dir = "./FPS_selected"
     os.makedirs(selected_dir, exist_ok=True)

     coord_indx=np.array([],dtype='int16')
     i=0
     while i <= selector.n_to_select-1 :
           coord=takeout_coordindex(df,selected_index[i])
           coord_indx=np.append(coord_indx,coord)
           src_path = os.path.join(xsf_directory, coord)
           dst_path = os.path.join(selected_dir, coord)
           shutil.copy(src_path, dst_path)
           i=i+1


     C=coord_indx.reshape(-1,1)


     file = open("coords_tobe_extracted.dat", "w+")
     string = "\n ".join(map(str, coord_indx))
     file.write(string)
     file.close()

     with open('animation.axsf','w') as file:
          file.write(f"ANIMSTEPS {len(coord_indx)}\n")
          n=0
          for file_name in coord_indx:
              atoms, coords, gradients, total_energy = read_xsf(os.path.join(xsf_directory, file_name))
              n=n+1
              file.write(f"ATOMS {n}\n")
              for atom, coord in zip(atoms, coords):
                  file.write(f"{atom} {coord[0]:.4f} {coord[1]:.4f} {coord[2]:.4f}\n")
    

     with open('animation.xyz','w') as file:
     #file.write(f"ANIMSTEPS {len(coord_indx)}\n")
          n=0
          for file_name in coord_indx:
              atoms, coords, gradients, total_energy = read_xsf(os.path.join(xsf_directory, file_name))
              n=n+1
              file.write(f"{len(atoms)}\n")
              file.write(f"{file_name}\n")
              for atom, coord in zip(atoms, coords):
                  file.write(f"{atom} {coord[0]:.4f} {coord[1]:.4f} {coord[2]:.4f}\n")
    
     print("FPS selection done.\nSelected structure xsf files are copied in FPS_structures folder.\n###########################################################################################\nSelected structure names are in 'coords_tobe_extracted.dat' file.\nAnimation files 'animation.axsf' and 'animation.xyz' are also generated for visualization.\n###########################################################################################")

#furthest_point_sampling(xsf_dir=xsf_directory, FPS_structures=50)   
