from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

version = '0.13'

install_requires = [
        'pyramid >=1.6a2',
        ]

tests_require = [
        'pytest',
        'WebTest',
        'mock',
        'colander',
        'jsonschema',
        'pyramid_sqlalchemy >=1.2',
        'pyramid_tm',
        ]


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(name='rest_toolkit',
      version=version,
      description='REST toolkit',
      long_description=open('README.rst').read() + '\n' +
              open('changes.rst').read(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Framework :: Pyramid',
          'Intended Audience :: Developers',
          'License :: DFSG approved',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Internet :: WWW/HTTP :: WSGI',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='REST Pyramid',
      author='Wichert Akkerman',
      author_email='wichert@wiggy.net',
      url='https://github.com/wichert/rest_toolkit',
      license='BSD',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=True,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'tests': tests_require},
      cmdclass={'test': PyTest},
      )
