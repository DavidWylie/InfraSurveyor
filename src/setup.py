from setuptools import setup

setup(
    name='surveyor',
    version='0.1',
    py_modules=['surveyor'],
    install_requires=[
        'click',
        'boto3',
        'pygraphviz'
    ],
    entry_points='''
        [console_scripts]
        surveyor=surveyor:cli
    ''',
)