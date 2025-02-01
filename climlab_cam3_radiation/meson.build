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

inc_np = include_directories(incdir_numpy, incdir_f2py, 'src')

fortsources = files(
                'src/pmgrid.F90',
                'src/prescribed_aerosols.F90',
                'src/shr_kind_mod.F90',
                'src/quicksort.F90',
                'src/abortutils.F90',
                'src/absems.F90',
                'src/wv_saturation.F90',
                'src/aer_optics.F90',
                'src/cmparray_mod.F90',
                'src/shr_const_mod.F90',
                'src/physconst.F90',
                'src/pkg_cldoptics.F90',
                'src/gffgch.F90',
                'src/chem_surfvals.F90',
                'src/volcrad.F90',
                'src/radae.F90',
                'src/radlw.F90',
                'src/radsw.F90',
                'src/crm.F90',
                'Driver.f90',
)

cam3module = custom_target('_cam3.c',
  input : ['src/shr_kind_mod.F90', 'src/absems.F90', 'Driver.f90'],
  output : ['_cam3module.c',
            '_cam3-f2pywrappers2.f90',
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