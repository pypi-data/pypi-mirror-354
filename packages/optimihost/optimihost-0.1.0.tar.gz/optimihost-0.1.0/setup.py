from setuptools import setup, find_packages

setup(
    name='optimihost',
    version='0.1.0',
    description='Optimihost Pterodactyl Panel API wrapper',
    author='OptimiHost UG',
    packages=find_packages(),
    install_requires=['py-dactyl>=2.0.4'],
    python_requires='>=3.6',
)
