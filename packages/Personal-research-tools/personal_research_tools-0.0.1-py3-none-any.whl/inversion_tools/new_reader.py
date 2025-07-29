import os.path 
import numpy as np # type: ignore
### Functions for GS 1DHe
def getFilePaths(code=str, temp=str, molecule=str, methodName=str):
    """
    Reads data for the GS molecule
    """
    default_preMethod_path = os.path.join('~', 'Desktop','Inversions_testing', code, temp, molecule)
    dens_path = os.path.expanduser(os.path.join(default_preMethod_path, methodName, 'static', 'density.y=0,z=0'))
    vks_path = os.path.expanduser(os.path.join(default_preMethod_path, methodName, 'static', 'vks.y=0,z=0'))
    vxc_path = os.path.expanduser(os.path.join(default_preMethod_path, methodName, 'static', 'vxc.y=0,z=0'))
    vh_path = os.path.expanduser(os.path.join(default_preMethod_path, methodName, 'static', 'vh.y=0,z=0'))
    return dens_path, vks_path, vxc_path, vh_path
def getData(code=str, temp=str, molecule=str, methodName=str): 
    """
    Reads data for the GS molecule
    """
    dens_path, vks_path, vxc_path, vh_path = getFilePaths(code, temp, molecule, methodName)
    x_grid = np.loadtxt(dens_path)[:,0]  # 1D grid
    dens = np.loadtxt(dens_path)[:,1]
    vks = np.loadtxt(vks_path)[:,1]
    vxc = np.loadtxt(vxc_path)[:,1]
    vh = np.loadtxt(vh_path)[:,1]
    return x_grid, dens, vks, vxc, vh
