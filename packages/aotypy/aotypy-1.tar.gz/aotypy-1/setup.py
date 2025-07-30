from setuptools import find_packages, setup

setup(
    name='aotypy',
    packages=find_packages(include=['aotylib']),
    version='1',
    description='get info about albums and artists from albumoftheyear.org',
    author='cbhy',
    install_requires=['beautifulsoup4==4.13.4','cloudscraper==1.2.71','requests==2.32.4'],
)