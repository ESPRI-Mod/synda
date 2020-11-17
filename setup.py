from setuptools import setup
from setuptools import find_packages

setup(
    name='synda',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'synda/data': ['synda/data_package/data.tar.gz'],
    },
    entry_points={
        "console_scripts": [
            "synda=synda.bin.main:run"
        ]
    },
    url='https://github.com/Prodiguer/synda',
    version='3.15',
    description='ESGF Data transfer Program',
    long_description='This program download files from the Earth System Grid Federation (ESGF) '
                     'archive using command line.',
    zip_safe=False,
    license='Public',
    platforms='Linux',
    maintainer='abennasser',
    maintainer_email='abennasser@ipsl.fr')
