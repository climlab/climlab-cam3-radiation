project('climlab_cam3_radiation', 'c')

add_languages('fortran')
# Add Fortran compiler flags globally
add_project_arguments(
    '-fdefault-real-8',
    language: 'fortran'
)

py = import('python').find_installation(pure: false)
py_dep = py.dependency()

subdir('climlab_cam3_radiation')