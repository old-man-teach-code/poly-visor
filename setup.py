from setuptools import setup, find_packages
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('polyvisor/build/')

setup(
    name='polyvisor',
    version='0.0.1',
    packages=find_packages(),
    package_data={
        "polyvisor": extra_files
    },
    install_requires=[
        'requests',
        'importlib; python_version == "3.10"',
    ],
)
