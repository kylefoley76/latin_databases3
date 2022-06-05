

from setuptools import setup

setup(
    name='Latin_Databases',
    version='0.1.0',
    description='Merges several Latin databases into one',
    url='https://github.com/kylefoley76/latin_database',
    author='Kyle Foley',
    author_email='kylefoley202@gmail.com',
    license='non-profitable',
    packages=['pyexample'],
    install_requires=['Levenshtein',
                      'striprtf==0.0.12',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Humanities/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
    ],
)
