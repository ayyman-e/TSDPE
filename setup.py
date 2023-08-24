from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("requirements-dev.txt") as f:
    dev_requirements = f.read().splitlines()

setup(
    name='TSDPE',
    author='Ayman Elhalwagy',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
    extras_require = {
        'dev': dev_requirements
    }
    # And any other metadata you want to include
)