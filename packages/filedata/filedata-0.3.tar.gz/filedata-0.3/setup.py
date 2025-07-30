import re
import sys
from os.path import join, dirname

from setuptools import setup, find_packages

with open(join(dirname(__file__), 'README.rst'), 'r', encoding='utf-8') as fd:
    long_description = fd.read()

install_requires = [
    'lxml>=4.6.3',
    'cssselect>=1.1.0',
    'PyMuPDF>=1.21.1',
    'Pillow>=9.4.0',
    'requests-toolbelt>=0.9.1',
    'pydantic>=1.8.1',
    'opencv-python>=4.6.0.66',
]


def read_version():
    p = join(dirname(__file__), 'filedata', '__init__.py')
    with open(p, 'r', encoding='utf-8') as f:
        return re.search(r"__version__ = '([^']+)'", f.read()).group(1)


def main():
    if sys.version_info < (3, 6):
        raise RuntimeError('The minimal supported Python version is 3.6')

    setup(
        name='filedata',
        version=read_version(),
        description='Utils for extracting data from files',
        long_description=long_description,
        author='jadbin',
        author_email='jadbin.com@hotmail.com',
        zip_safe=False,
        packages=find_packages(exclude=('tests',)),
        include_package_data=True,
        python_requires='>=3.6',
        install_requires=install_requires,
        entry_points={
        },
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Intended Audience :: Developers',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )


if __name__ == '__main__':
    main()
