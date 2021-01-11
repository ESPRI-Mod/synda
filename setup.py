from setuptools import setup
from setuptools import find_packages

from synda.version import CURRENT as VERSION
setup(
    name='synda',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "synda=synda.sdt.main:run"
        ]
    },
    url='https://github.com/Prodiguer/synda',
    version=VERSION,
    description='ESGF Data transfer Program',
    long_description='This program download files from the Earth System Grid Federation (ESGF) '
                     'archive using command line.',
    zip_safe=False,
    license='Public',
    platforms='Linux',
    maintainer='abennasser',
    maintainer_email='abennasser@ipsl.fr')
