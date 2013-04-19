from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name='hydedown',
    version='0.1.1',
    author='Lakshmi Vyas',
    author_email='lakshmi.vyas@gmail.com',
    url='http://github.com/hyde/hydedown',
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
    packages=find_packages(),
    install_requires=['Markdown==2.3.1'],
    tests_require=(
        'nose',
      ),
    test_suite='nose.collector',
)