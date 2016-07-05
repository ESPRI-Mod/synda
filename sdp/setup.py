from distutils.core import setup
import glob
import os
setup(name='sdp',
        #py_modules=['ppdb'],
        scripts=[os.path.join('bin',f) for f in os.listdir('bin')], 
        data_files=[('conf',['conf/sdp.conf']),
                    ('conf/pipeline',glob.glob(os.path.join('conf/pipeline', '*'))),
                    ('doc',['doc/LICENSE']),
                    ('tools', glob.glob(os.path.join('tools', '*'))),
                    ('data',''),
                    ('log',''),
                    ('tmp',''),
                    ('db','')], 
        url='https://github.com/Prodiguer/synda',
        version='1.1',
        description='ESGF Data Processing Program',
        long_description='This program processes files from the Earth System Grid Federation (ESGF) archive.',
        license='Public',
        platforms='Linux',
        author='jripsl',
        author_email='jripsl@ipsl.jussieu.fr'
        )
