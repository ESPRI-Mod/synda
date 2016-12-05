#from setuptools import setup
from distutils.core import setup
import glob
import os

setup(name='sdp',
        #py_modules=['ppdb'],
        scripts=[os.path.join('bin',f) for f in os.listdir('bin')], 
        data_files=[('conf',['conf/sdp.conf']),
                    ('conf',['conf/credentials.conf']),
                    ('conf/pipeline',glob.glob(os.path.join('conf/pipeline', '*.py'))),
                    ('doc',['doc/LICENSE']),
                    ('data',''),
                    ('log',''),
                    ('tmp',''),
                    ('db','')], 
        url='https://github.com/Prodiguer/synda',
        version='1.3',
        description='ESGF Data Processing Program',
        long_description='This program processes files from the Earth System Grid Federation (ESGF) archive.',
        license='Public',
        platforms='Linux',
        maintainer='jripsl',
        maintainer_email='jripsl@ipsl.jussieu.fr',
        author='jripsl',
        author_email='jripsl@ipsl.jussieu.fr'
        )
