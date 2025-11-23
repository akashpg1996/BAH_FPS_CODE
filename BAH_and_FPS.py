from BAH_FPS.BAH import generate_BAH_dataset
from BAH_FPS.FPS import furthest_point_sampling
import warnings
warnings.filterwarnings("ignore",message='X does not have valid feature names, but FPS was fitted with feature names')


#Please write the path where .xsf files are located and number of FPS structures to be selected.
xsf_directory = "/home/akash/work/VSCODE/BAH_FPS/BAH_FPS_CODE/test/testset"
FPS_structures=25


hash_table,random_index,BAH_dir = generate_BAH_dataset(xsf_dir=xsf_directory,divs=10,ncpu=4)
furthest_point_sampling(xsf_dir=BAH_dir, FPS_structures=FPS_structures)
