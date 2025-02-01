python_sources = [
  '__init__.py',
]

py.install_sources(
  python_sources,
  pure: false,
  subdir: 'climlab_cam3_radiation'
)

incdir_numpy = run_command(py,
  ['-c', 'import os; os.chdir(".."); import numpy; print(numpy.get_include())'],
  check : true
).stdout().strip()

incdir_f2py = run_command(py,
    ['-c', 'import os; os.chdir(".."); import numpy.f2py; print(numpy.f2py.get_include())'],
    check : true
).stdout().strip()

inc_np = include_directories(incdir_numpy, incdir_f2py)


fortsources = files('pmgrid.F90',
                'prescribed_aerosols.F90',
                'shr_kind_mod.F90',
                'quicksort.F90',
                'abortutils.F90',
                'absems.F90',
                'wv_saturation.F90',
                'aer_optics.F90',
                'cmparray_mod.F90',
                'shr_const_mod.F90',
                'physconst.F90',
                'pkg_cldoptics.F90',
                'gffgch.F90',
                'chem_surfvals.F90',
                'volcrad.F90',
                'radae.F90',
                'radlw.F90',
                'radsw.F90',
                'crm.F90',
                'Driver.f90',
)

cam3module = custom_target('_cam3.c',
  input : ['shr_kind_mod.F90', 'absems.F90', 'Driver.f90'],
  output : ['_cam3module.c',
            '_cam3-f2pywrappers2.f90',
             '_cam3-f2pywrappers.f',
  ],
  command : [py, '-m', 'numpy.f2py', '@INPUT@', 
             '-m', '_cam3', '--lower', 
             '--build-dir', '@OUTDIR@']
)

cam3_library = static_library(
  'cam3',
  fortsources,
  include_directories: inc_np
)

py.extension_module('_cam3',
  sources: [
    cam3module,
    incdir_f2py / 'fortranobject.c'
  ],
  include_directories: inc_np,
  link_with: cam3_library,
  dependencies : py_dep,
  install : true,
  subdir: 'climlab_cam3_radiation'
)

subdir('tests')