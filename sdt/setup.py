import os

from setuptools import setup
setup(
    name='synda',
    scripts=[os.path.join('bin', f) for f in os.listdir('bin')],
    include_package_data=True,
    package_data={
        'data': ['data_package/data.tar.gz'],
    },
    entry_points={
        "console_scripts": [
            "synda=synda:run"
        ]
    },
    url='https://github.com/Prodiguer/synda',
    version='3.12',
    description='ESGF Data transfer Program',
    long_description='This program download files from the Earth System Grid Federation (ESGF) '
                     'archive using command line.',
    zip_safe=False,
    license='Public',
    platforms='Linux',
    maintainer='abennasser',
    maintainer_email='abennasser@ipsl.fr')
