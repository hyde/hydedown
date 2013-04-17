from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name='hyde-markdown-extensions',
    version='0.1',
    author='Lakshmi Vyas',
    author_email='lakshmi.vyas@gmail.com',
    url='http://github.com/hyde/hyde-markdown-extensions',
    description='Markdown extensions that facilitate hyde website generation',
    long_description=long_description,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    provides=['hyde'],
    install_requires=['Markdown==2.3.1'],
    tests_require=(
        'nose',
      ),
    test_suite='nose.collector',
)