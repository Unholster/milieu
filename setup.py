# coding=utf_8
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name= "unholster.milieu",
    version= "1.0.0",
    author = u"Sebastian Acuña",
    author_email = "sebastian@unholster.com",
    maintainer = u"Andrés Villavicencio",
    maintainer_email = "andres@unholster.com",
    packages = find_packages(),
    license = "BSD",
    package_data={
        'milieu' : [
            '*.*',
        ]
    },
    url="https://github.com/Unholster/milieu",
    install_requires =[],
    description="Flexible parameter management",
    long_description=read("README.md"),
    classifiers=["Development Status :: 5 - Production/Stable", "Topic :: Utilities"]
)