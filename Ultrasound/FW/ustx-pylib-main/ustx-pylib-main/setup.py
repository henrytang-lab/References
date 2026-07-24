from setuptools import setup, find_packages

setup(
    name='ustx-pylib',
    version='0.1.0',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pyserial",  
    ],
    description="Openwater USTX python library",
    author="George Vigelette",
    author_email="george@openwater.cc",
    url="https://github.com/OpenwaterInternet/ustx-pylib.git",
)
