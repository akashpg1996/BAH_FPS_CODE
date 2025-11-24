import numpy as np 
import math
import pandas as pd
from multiprocessing import Pool, cpu_count

def read_xsf(xsf_file):
    atoms = []
    coords = []
    gradients = []
    total_energy = None
    with open(xsf_file, 'r') as f:
        lines = f.readlines()

        # Extract total energy
        for line in lines:
            if line.startswith('# total energy'):
                total_energy = float(line.split('=')[1].strip().split()[0])
                break

        # Read ATOMS section
        atoms_section = False
        for line in lines:
            if line.strip() == "ATOMS":
                atoms_section = True
                continue
            if atoms_section:
                parts = line.split()
                if len(parts) == 7:
                    atom_symbol = parts[0]
                    coord = [float(x) for x in parts[1:4]]
                    grad = [float(x) for x in parts[4:]]
                    atoms.append(atom_symbol)
                    coords.append(coord)
                    gradients.append(grad)

    return atoms, coords, gradients, total_energy

def distance(i,j,coords):
    coord1 = np.array(coords[i][:])
    coord2 = np.array(coords[j][:])
    distance = np.linalg.norm(coord2 - coord1)
    return distance
    
def get_CM(natoms,atoms, coords):
    coulomb_matrix= np.zeros((natoms,natoms))
    atomic_number_dict = {
    'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10,
    'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20,
    'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30,
    'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36, 'Rb': 37, 'Sr': 38, 'Y': 39, 'Zr': 40,
    'Nb': 41, 'Mo': 42, 'Tc': 43, 'Ru': 44, 'Rh': 45, 'Pd': 46, 'Ag': 47, 'Cd': 48, 'In': 49, 'Sn': 50,
    'Sb': 51, 'I': 53, 'Te': 52, 'Xe': 54, 'Cs': 55, 'Ba': 56, 'La': 57, 'Ce': 58, 'Pr': 59, 'Nd': 60,
    'Pm': 61, 'Sm': 62, 'Eu': 63, 'Gd': 64, 'Tb': 65, 'Dy': 66, 'Ho': 67, 'Er': 68, 'Tm': 69, 'Yb': 70,
    'Lu': 71, 'Hf': 72, 'Ta': 73, 'W': 74, 'Re': 75, 'Os': 76, 'Ir': 77, 'Pt': 78, 'Au': 79, 'Hg': 80,
    'Tl': 81, 'Pb': 82, 'Bi': 83, 'Po': 84, 'At': 85, 'Rn': 86, 'Fr': 87, 'Ra': 88, 'Ac': 89, 'Th': 90,
    'Pa': 91, 'U': 92, 'Np': 93, 'Pu': 94, 'Am': 95, 'Cm': 96, 'Bk': 97, 'Cf': 98, 'Es': 99, 'Fm': 100,
    'Md': 101, 'No': 102, 'Lr': 103, 'Rf': 104, 'Db': 105, 'Sg': 106, 'Bh': 107, 'Hs': 108, 'Mt': 109,
    'Ds': 110, 'Rg': 111, 'Cn': 112, 'Nh': 113, 'Fl': 114, 'Mc': 115, 'Lv': 116, 'Ts': 117, 'Og': 118
}
    for i in range(natoms):
        for j in range(natoms):
            if i==j:
                coulomb_matrix[i][j]= 0.5*(atomic_number_dict[atoms[i]])**2.4
            if i!=j:
                coulomb_matrix[i][j]= (atomic_number_dict[atoms[i]])*(atomic_number_dict[atoms[j]])/distance(i,j,coords)
    return coulomb_matrix

def takeout_coordindex(df,random_index):
    coord=df.iloc[random_index,0]
    return coord

def nint(x):
    return math.floor(x + 0.5) if x > 0 else math.ceil(x - 0.5)

# Function to process one column
def process_column(args):
    i, X_col, divs = args  # Unpack arguments
    rho_min = X_col.min()
    rho_max = X_col.max()
    Y_col = np.zeros_like(X_col, dtype=int)
    
    if rho_min != rho_max:
        Y_col = [nint(divs * ((rho_max - x) / (rho_max - rho_min))) for x in X_col]
    return i, Y_col

# Multiprocessing main function
def parallel_process(X, divs,threads):
    num_columns = X.shape[1]
    args = [(i, X.iloc[:, i], divs) for i in range(num_columns)]
    
    with Pool(threads) as pool:
        results = pool.map(process_column, args)
    
    # Create an empty DataFrame for results
    Y = pd.DataFrame(np.zeros_like(X, dtype=int), columns=X.columns)
    for i, Y_col in results:
        Y.iloc[:, i] = Y_col
    
    return Y
