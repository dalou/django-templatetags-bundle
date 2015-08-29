#from __future__ import print_function
import ast
import os
import sys
import codecs
import subprocess
from fnmatch import fnmatchcase
from distutils.util import convert_path
from setuptools import setup, find_packages


def find_version(*parts):
    version_py = os.path.join(os.path.dirname(__file__), 'version.py')


    try:
        version_git = subprocess.check_output(["git", "tag"]).rstrip().splitlines()[-1]
    except:
        with open(version_py, 'wrb') as fh:
            version_git = open(version_py, 'rb').read().strip().split('=')[-1].replace('"','')

    version_msg = "# Do not edit this file, pipeline versioning is governed by git tags" + os.linesep + "# following PEP 386"
    with open(version_py, 'wrb') as fh:
        fh.write(version_msg + os.linesep + '__version__ = "%s"' % version_git)

    return "{ver}".format(ver=version_git)

def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()



# Provided as an attribute, so you can append to these instead
# of replicating them:
standard_exclude = ('*.py', '*.pyc', '*$py.class', '*~', '.*', '*.bak')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build',
                                './dist', 'EGG-INFO', '*.egg-info')

setup(
    name='django-templatetags-bundle',
    version=find_version(),
    description='Django templatetags extra bundles',
    long_description=read('README.rst'),
    author='Autrusseau Damien',
    author_email='autrusseau.damien@gmail.com',
    url='http://github.com/dalou/django-templatetags-bundle',
    packages=find_packages(),
    zip_safe=False,
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    test_suite='runtests.runtests',
    install_requires=[
        'django >= 1.8.4, <= 1.9',
        'babel >= 2.0',
    ],
)