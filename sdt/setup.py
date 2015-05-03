#from setuptools import setup
from distutils.core import setup
import glob
import os
setup(name='sdt',
		#py_modules=['sdutils'],
		scripts=[os.path.join('bin',f) for f in os.listdir('bin')],
		data_files=[('conf',['conf/sdt.conf']),
                    ('selection', glob.glob(os.path.join('selection', '*.txt'))),
                    ('selection/sample', glob.glob(os.path.join('selection/sample', '*'))),
                    ('doc',['doc/LICENSE']),
                    ('tools', glob.glob(os.path.join('tools', '*'))),
                    ('data',''),
                    ('log',''),
                    ('tmp',''),
                    ('db','')], 
		url='https://github.com/Prodiguer/synda',
		version='3.0',
		description='ESGF Data transfer Program',
		long_description='This program download files from the Earth System Grid Federation (ESGF) archive using command line.',
		license='Public',
		platforms='Linux',
		author='Jerome Raciazek',
		author_email='jerome.raciazek@ipsl.jussieu.fr'
		)
