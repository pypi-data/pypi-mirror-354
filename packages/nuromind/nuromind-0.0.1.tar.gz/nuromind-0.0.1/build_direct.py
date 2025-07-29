import os
import shutil
from setuptools import setup, find_packages
from wheel.bdist_wheel import bdist_wheel

# Clean
for d in ['dist', 'build', 'src/nuromind.egg-info']:
    if os.path.exists(d):
        shutil.rmtree(d)

# Setup args
setup_args = {
    'name': 'nuromind',
    'version': '0.0.1',
    'author': 'Ziyuan Huang',
    'author_email': 'ziyuan.huang2@umassmed.edu',
    'description': 'A neuroscience ML library',
    'packages': find_packages(where='src'),
    'package_dir': {'': 'src'},
    'python_requires': '>=3.8',
}

# Build
setup(**setup_args, script_args=['bdist_wheel', 'sdist'])