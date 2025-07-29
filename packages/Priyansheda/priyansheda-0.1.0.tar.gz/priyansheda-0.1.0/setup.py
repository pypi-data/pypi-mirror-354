
from setuptools import setup, find_packages

setup(
    name='Priyansheda',
    version='0.1.0',
    description='Automated bivariate analysis and visualization tools for EDA',
    author='Priyanshu Raj',
    author_email='priyanshujha274@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scipy',
        'matplotlib',
        'seaborn'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

