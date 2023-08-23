from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='TSDPE',
    author='Ayman Elhalwagy',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
    # And any other metadata you want to include
)