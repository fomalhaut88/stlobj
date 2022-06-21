import sys
from distutils.core import setup
from setuptools import find_packages


scripts = [
    'bin/stl2obj.py',
    'bin/obj2stl.py',
]
if sys.platform == 'win32':
    scripts.append('bin/stl2obj.cmd')
    scripts.append('bin/obj2stl.cmd')
else:
    scripts.append('bin/stl2obj')
    scripts.append('bin/obj2stl')

setup(
    name='stlobj',
    version='1.0',
    packages=find_packages(),
    license="Free",
    long_description=open('README.md').read(),
    scripts=scripts,
    install_requires=[
        'numpy==1.22.0',
    ],
)
