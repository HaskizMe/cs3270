from setuptools import setup, find_packages

setup(
    name='weather_stats_bh',  # Name of your module
    version='0.1',  # Version of your module
    packages=find_packages(),  # Automatically find packages
    description='Weather stats',
    author='Bailey Haskell',
    author_email='',
    url='',  # Project URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',  # Minimum Python version
)