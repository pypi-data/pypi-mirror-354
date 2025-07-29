from setuptools import setup, find_packages

setup(
name='ml1_10',
version='0.1.0',
packages=find_packages(),
install_requires=[
'pandas',
'numpy',
'matplotlib',
'seaborn',
'scikit-learn'
],  
author='veeresh',
author_email='veeresh04@gmail.com',
description='ML tool for data visualization and outlier detection',
long_description=open('README.md').read(),
long_description_content_type='text/markdown',
url='https://github.com/Veeresh-hp/ml1_10',
classifiers=[
'Programming Language :: Python :: 3',
'Operating System :: OS Independent',
],
python_requires='>=3.7',
)