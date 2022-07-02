
import sys,os
import urllib.request
import requests
from setuptools import setup
from pathlib import Path
from setuptools.command.develop import develop
from setuptools.command.install import install

vol2 = os.path.join(os.path.dirname(__file__)) + '/latin/'
vol3 = os.path.join(os.path.dirname(__file__)) + '/latin/general_la/'
sys.path.append(vol2)
sys.path.append(vol3)
fold = f'{vol3}files/'

this_directory = Path(__file__).parent
long_description = ( this_directory/ "README.md").read_text()


def temp():
    #print('running post installation')
    # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
    s = 'https://storage.googleapis.com/download/storage/v1/b/deduction4/o/on%20cicero.txt?generation=1656578017964238&alt=media'
    urllib.request.urlopen(s)
    if not os.path.exists(fold):
        os.mkdir(fold)
    file = f'{fold}hey.txt'
    r = requests.get(s, stream=True, verify=False)
    if r.status_code == 200:
        r.raw.decode_content = 1
        with open(file, 'wb') as f:
            f.write(r.content)
    else:
        print('failed to download data files')


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        temp()


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        temp()

setup(
    name='latin_databases',
    version='0.1.14',
    description='none',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kylefoley76/latin_databases3',
    author='Kyle Foley',
    author_email='kylefoley202@gmail.com',
    license='BSD',
    zip_safe=False,
    packages=['latin','latin/general_la','latin/unidecode2'],
    install_requires=['Levenshtein',
                      'striprtf==0.0.14',
                      ],
    cmdclass={
            'develop': PostDevelopCommand,
            'install': PostInstallCommand,
        },

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.8',
    ],
)

