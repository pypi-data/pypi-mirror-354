
from setuptools import setup, find_packages

setup(
    name='alumathpeergroup17',
    version='0.1.4',
    author='WilsonsNavid',
    author_email='wadotiwawil@gmail.com',
    description='A basic matrix computation library for addition, subtraction, and multiplication.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords='matrix addition subtraction multiplication linear-algebra',
    python_requires='>=3.6',
    license='MIT',  # ✅ Correct way
)
