import os
import numpy as np 
from ase import Atom, Atoms
#------------------------------------------------------------------------------------------
hartree2eV = 27.211386245981 #NIST
bohr2angstrom=0.529177210544 #NIST
eVtokcalpermol=23.060548012069496
hartree2kcalmol=627.5094738898777
#------------------------------------------------------------------------------------------
def get_termination_orca(pathfilename):
    if os.path.isfile(pathfilename):
        normal=0
        file=open(pathfilename,'r')
        for line in file:
            if "ORCA TERMINATED NORMALLY" in line: normal=normal+1
        file.close()
        return normal
    else:
        return False
#------------------------------------------------------------------------------------------
def get_geometry_orca(pathfilename):
    nt=get_termination_orca(pathfilename)
    if nt==False: return False
    filename=os.path.basename(pathfilename)
    namein=filename.split('.')[0]
    trajectory = get_traj_orca(pathfilename,False)
    enemin = float('inf')
    for i, atoms in enumerate(trajectory):
        energy=atoms.info.get('e', 0.0)
        if energy < enemin:
            enemin=energy
            poscar=atoms.copy()
            poscar.info['c']=nt
            poscar.info['e']=energy
            poscar.info['i']=namein
    return (poscar)
#------------------------------------------------------------------------------------------
def get_traj_orca(pathfilename, force=False):
    filename = os.path.basename(pathfilename)
    namein=filename.split('.')[0]
    start, end, ene, start_2, end_2 = [], [], [], [], []
    openold = open(pathfilename,"r")
    rline = openold.readlines()
    for i in range(len(rline)):
        if "CARTESIAN COORDINATES (ANGSTROEM)" in rline[i]:
            start.append(i+2)
            for j in range(i + 2, len(rline)):
                if rline[j].strip() == "":
                    end.append(j - 1)
                    break
        if "TOTAL SCF ENERGY" in rline[i]:
            eneline = rline[i+3].split()
            ene.append(eneline[5]) #ENERGY IN ELECTROVOLT

        if "CARTESIAN GRADIENT" in rline[i] and force:
            start_2.append(i+3)
            for j in range(i + 3, len(rline)):
                if rline[j].strip() == "":
                    end_2.append(j - 1)
                    break
    moleculeout=[]
    for i,iStart in enumerate(start[:-1]):
        singlemol = Atoms()
        singlemol.info['e'] = float(ene[i]) #ENERGY IN ELECTROVOLT
        singlemol.info['i'] = namein+'_'+str(i+1).zfill(3)
        for line in rline[start[i] : end[i]+1]:
            words = line.split()
            ss = str(words[0])
            xc,yc,zc = float(words[1]), float(words[2]), float(words[3])
            ai=Atom(symbol=ss,position=(xc, yc, zc))
            singlemol.append(ai)
        if force:
            forces_list_by_group = []
            for line in rline[start_2[i] : end_2[i]+1]:
                words = line.split()
                fx,fy,fz = float(words[3]), float(words[4]), float(words[5])
                fx=-fx*hartree2eV/bohr2angstrom
                fy=-fy*hartree2eV/bohr2angstrom
                fz=-fz*hartree2eV/bohr2angstrom
                #IN ev/A
                forces_list_by_group.append([fx,fy,fz])    
            singlemol.arrays['forces'] = np.array(forces_list_by_group)
        moleculeout.extend([singlemol])
    openold.close()
    return (moleculeout)
#------------------------------------------------------------------------------------------
