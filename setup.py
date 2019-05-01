import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="responsysrest",
    version="0.1.12",
    author="Dan Black",
    author_email="dyspop@gmail.com",
    description="Python client library for the Responsys Interact REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dyspop/responsysrest",
    install_requires=['requests'],
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Framework :: Flake8',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
