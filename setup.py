from setuptools import setup

setup(
    name='stl',
    description='A personal information logging and collection system.',
    version='2.0.dev',
    license='Apache',
    url='http://cyborginstitute.org/projects/stl',
    packages=['stl'],
    entry_points={
        'console_scripts': [ 
            'stl = stl.stl:main',
            'sauron = stl.sauron:main',
            'lnote = stl.lnote:main',
            'wc-track = stl.wc_track:main'
            ]
        }
    )
