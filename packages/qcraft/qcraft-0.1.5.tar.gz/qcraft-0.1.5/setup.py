from setuptools import setup, find_packages
import os

with open("README_PYPI.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='qcraft',
    version='0.1.5',
    description='Qcraft: Quantum Circuit Design, Optimization, and Surface Code Mapping Platform',
    long_description=long_description,
    long_description_content_type="text/markdown",

    author='Debasis Mondal',
    packages=find_packages(),
    install_requires=[
        'PySide6',
        'PyYAML',
        'jsonschema',
        'networkx',
        'matplotlib',
        'numpy',
        'stable-baselines3',
        'scikit-learn',
        'pandas',
        'torch',
        'gymnasium',
        'stim',
        'pymatching',
        'qiskit>=1.0',
        'qiskit-aer',
        'qiskit-ibm-runtime',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'qcraft = circuit_designer.gui_main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'scode': ['code_switcher/*.py'],
        'configs': ['*.json', '*.yaml'],
    },
) 
