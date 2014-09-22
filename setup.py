from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='ccommander',
    version='0.0.1',
    description='Python wrapper for cirrus7\'s light commander API',
    long_description=readme(),
    url='https://github.com/kpj/CCommander',
    author='kpj',
    author_email='kpjkpjkpjkpjkpjkpj@gmail.com',
    license='MIT',
    packages=find_packages(),
    zip_safe=True,
    scripts=['bin/ccommander'],
    install_requires=['pyserial']
)
