from setuptools import setup
import os

setup(
    name='synda',
    scripts=[os.path.join('bin', f) for f in os.listdir('bin')],
    include_package_data=True,
    package_data={
        'data': ['data_package/data.tar.gz'],
    },
    url='https://github.com/Prodiguer/synda',
    version='3.11',
    description='ESGF Data transfer Program',
    long_description='This program download files from the Earth System Grid Federation (ESGF) '
                     'archive using command line.',
    zip_safe=False,
    license='Public',
    platforms='Linux',
    maintainer='abennasser',
    maintainer_email='abennasser@ipsl.fr')
