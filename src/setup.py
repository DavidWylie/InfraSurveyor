from setuptools import setup, find_packages

setup(
    name='surveyor',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'boto3',
        'pygraphviz'
    ],
    entry_points='''
        [console_scripts]
        surveyor=surveyor.main:cli
    ''',
)