

from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = ( this_directory/ "README.md").read_text()

setup(
    name='latin_databases',
    version='0.1.2',
    description='none',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kylefoley76/latin_databases3',
    author='Kyle Foley',
    author_email='kylefoley202@gmail.com',
    license='BSD',
    zip_safe=False,
    packages=['latin','latin/general_la'],
    install_requires=['Levenshtein',
                      'striprtf==0.0.12',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.8',
    ],
)

