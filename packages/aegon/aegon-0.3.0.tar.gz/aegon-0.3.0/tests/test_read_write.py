from aegon.libcode   import read_out, write
from aegon.libposcar import molecule2poscar
document = read_out()
#-----------------------------------------------------------------------------------------
# EXAMPLE OF TRAJ 
example_gaussian_01 = document.traj('gaussian', 'Al10C2M1.out', force=True)
write.cfg(example_gaussian_01, 'traj_gaussian.cfg', force=True)
write.xyz(example_gaussian_01, 'traj_gaussian.xyz')
poscarlist = molecule2poscar(example_gaussian_01, 15.0)
write.poscar(poscarlist,'traj_gaussian.vasp', opt='C')

# EXAMPLE OF GEO
example_gaussian_02 = document.geo('gaussian', 'Al10C2M1.out')
write.cfg(example_gaussian_02,'geo_gaussian.cfg')
write.xyz(example_gaussian_02,'geo_gaussian.xyz')
poscarlist = molecule2poscar(example_gaussian_02, 15.0)
write.poscar(poscarlist,'geo_gaussian.vasp', opt='C')
#-----------------------------------------------------------------------------------------
# EXAMPLE OF TRAJ 
aselist = document.traj('orca', 'B20Be.out', force=True)
write.cfg(aselist, 'traj_orca.cfg', force=True)
write.xyz(aselist, 'traj_orca.xyz')
poscarlist = molecule2poscar(aselist, 15.0)
write.poscar(poscarlist,'traj_orca.vasp', opt='C')

# EXAMPLE OF GEO
aseobject = document.geo('orca', 'B20Be.out')
write.cfg(aseobject,'geo_orca.cfg')
write.xyz(aseobject,'geo_orca.xyz')
poscarlist = molecule2poscar(aseobject, 15.0)
write.poscar(poscarlist,'geo_orca.vasp', opt='C')
#-----------------------------------------------------------------------------------------
# EXAMPLE OF TRAJ 
aselist = document.traj('vasp', 'B10Be.outcar', force=True)
write.cfg(aselist, 'traj_vasp.cfg', force=True)
write.xyz(aselist, 'traj_vasp.xyz')
write.poscar(aselist,'traj_vasp.vasp', opt='C')

# EXAMPLE OF GEO
aseobject = document.geo('vasp', 'B10Be.outcar')
write.cfg(aseobject,'geo_vasp.cfg')
write.xyz(aseobject,'geo_vasp.xyz')
write.poscar(aseobject,'geo_vasp.vasp', opt='C')
#-----------------------------------------------------------------------------------------
# EXAMPLE OF GEO
aseobject = document.geo('gulp', 'LJ061.got')
write.cfg(aseobject,'geo_gulp.cfg')
write.xyz(aseobject,'geo_gulp.xyz')
write.poscar(aseobject,'geo_gulp.vasp', opt='C')
#-----------------------------------------------------------------------------------------
exit()
