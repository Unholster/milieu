from setuptools import setup, find_packages

setup(
    name="milieu",
    version="1.0.0",
    packages = find_packages(),
    package_data={
        'milieu' : [
            '*.*',
        ]
    },
    install_requires =[],
    long_description="Flexible parameter management"
)