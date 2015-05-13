from distutils.core import setup
import glob
import os
setup(name='sdp',
		#py_modules=['ppdb'],
		scripts=[os.path.join('bin',f) for f in os.listdir('bin')], 
		data_files=[('conf',['conf/sdp.conf']),
                    ('doc',['doc/LICENSE']),
                    ('tools', glob.glob(os.path.join('tools', '*'))),
                    ('script', glob.glob(os.path.join('script', '*'))),
                    ('data',''),
                    ('log',''),
                    ('tmp',''),
                    ('db','')], 
		url='http://dods.ipsl.jussieu.fr/jripsl/synchro_data',
		version='1.0',
		description='ESGF Data Processing Program',
		long_description='This program processes files from the Earth System Grid Federation (ESGF) archive.',
		license='Public',
		platforms='Linux',
		author='Jerome Raciazek',
		author_email='jerome.raciazek@ipsl.jussieu.fr'
		)
