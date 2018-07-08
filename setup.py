from setuptools import setup, find_packages

setup(
    name='webStash',
    version='0.0.5',
    description='Stashing the html for later',
    long_description='See docs on the github repo',
    author='Alex Sieusahai',
    author_email='alexsieu14@gmail.com',
    url='https://github.com/alexsieusahai/webStash',
    license='MIT License',
    packages=find_packages(exclude=('tests'))
)
