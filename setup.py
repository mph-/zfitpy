#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

tests_require = ['nose', 'flake8', 'flake8-bugbear', 'flake8-comprehensions', 'flake8-requirements']
    
setup(name='zfitpy',
      version='0.2',
      author='Michael Hayes',
      author_email='michael.hayes@canterbury.ac.nz',
      description='Electrical model fitting to impedance data',      
      long_description = long_description,
      long_description_content_type="text/markdown",
      url='https://eng-git.canterbury.ac.nz/mph/zfitpy',      
      download_url='https://eng-git.canterbury.ac.nz/mph/zfitpy',
      install_requires=['matplotlib',
                        'numpy',
                        'scipy',
                        'lcapy',
                        'setuptools',
      ],
      python_requires='>=3.6',
      extras_require={
          'test': tests_require,
          'doc': ['sphinx', 'ipython'],
          'release': ['wheel', 'twine'],
      },
      tests_require=tests_require,      
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'zfitpy=zfitpy.scripts.zfitpy:main',              
          ],
      },                    
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
          "Operating System :: OS Independent",
      ],
)      

