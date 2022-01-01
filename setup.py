from setuptools import find_packages, setup

setup(
    author='Petros Mitseas',
    name='assignment',
    version='0.1.0',
    packages=find_packages(include=['main', 'main.*']),
    install_requires=[
        'PyYAML',
        'pandas',
        'numpy',
        'matplotlib',
        'plotly',
        'jupyter'
    ]
)