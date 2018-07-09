from setuptools import setup, find_packages
from os import path

import responsysrest

project_dir = path.abspath(path.dirname(__file__))
with open(path.join(project_dir, 'README.md')) as f:
    long_description = f.read()

install_requires = (
    'requests'
)
tests_require = (
    'pytest',
    'coverage',
    'mock',
    'nose',
    'pep8',
    'pinocchio',
    'pyflakes'
)

setup(
    name=responsysrest.__name__,
    keywords=responsysrest.__keywords__,
    version=responsysrest.__version__,
    url='https://github.com/dyspop/responsysrest',
    author='Dan Black',
    author_email='dyspop@gmail.com',
    description='Python client library for the Responsys Interact REST API',
    long_description=long_description,
    packages=find_packages(),
    license='GPLv2',
    install_requires=install_requires,
    setup_requires=tests_require,
    tests_require=tests_require,
    test_suite='pytest',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Framework :: Flake8',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
