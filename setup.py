#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='zfitter',
      version='0.1.0',
      author='Michael Hayes',
      author_email='michael.hayes@canterbury.ac.nz',
      description='Impedance model fitting',      
      long_description = long_description,
      long_description_content_type="text/markdown",
      url='https://eng-git.canterbury.ac.nz/mph/zfitter',      
      download_url='https://eng-git.canterbury.ac.nz/mph/zfitter',
      install_requires=['matplotlib',
                        'numpy',
                        'scipy',
                        'lcapy'                        
      ],
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'zfitter=zfitter.scripts.zfitter:main',              
          ],
      },                    
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
          "Operating System :: OS Independent",
      ],
)      

