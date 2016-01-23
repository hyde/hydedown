from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''


def read_requirements(f):
    reqs = []
    with open(f, "r") as h:
        reqs = [req.split('#', 1)[0].strip() for req in h]
        reqs = [req for req in reqs if req]
    return reqs

install_requires = read_requirements('requirements.txt')

setup(
    name='hydedown',
    version='0.1.2',
    author='Hyde contributors',
    author_email='hyde-dev@googlegroups.com',
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
    install_requires=install_requires,
    tests_require=(
        'nose',
      ),
    test_suite='nose.collector',
)
