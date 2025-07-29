from setuptools import setup, find_packages

# read the contents of README.md file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


CP_VERSION = '2025.6.8'
LIBS_VERSION = "2025.6.8"


# print(find_packages())


setup(
  name = 'coppertop-bones-libs',
  install_requires=[
    f'coppertop-bones=={CP_VERSION}'
  ],
  version=LIBS_VERSION,
  packages = [
    'coppertop.dm',
    'coppertop.dm._core',
    'coppertop.dm.core',
    'coppertop.dm.finance',
    'coppertop.dm.frame',
    'coppertop.dm.linalg',
    'coppertop.dm.linalg.algos',
    'coppertop.dm.stdlib',
    'coppertop.dm.utils',
  ],
  # package_dir = {'': 'core'},
  # namespace_packages=['coppertop_'],
  python_requires = '>=3.11',
  license = 'OSI Approved :: Apache Software License',
  description = 'The dm and penfold standard libraries for coppertop and bones',
  long_description_content_type='text/markdown',
  long_description=long_description,
  author = 'David Briant',
  author_email = 'dangermouseb@forwarding.cc',
  url = 'https://github.com/coppertop-bones/coppertop-libs',
  download_url = '',
  # download_url = f'https://github.com/coppertop-bones/dm/archive/{version}.tar.gz', not maintained
  keywords = ['multiple', 'dispatch', 'piping', 'pipeline', 'pipe', 'functional', 'multimethods', 'multidispatch',
            'functools', 'lambda', 'curry', 'currying', 'dataframe', 'polars', 'pandas'],
  include_package_data=True,
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Science/Research',
    'Topic :: Utilities',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3.11',
  ],
  zip_safe=False,
)
