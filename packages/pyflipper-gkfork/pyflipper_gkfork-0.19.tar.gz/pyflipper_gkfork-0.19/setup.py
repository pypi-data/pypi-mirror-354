
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    readme = fh.read()

setuptools.setup(
  name = 'pyflipper_gkfork',      
  package_dir={'': 'src'},
  packages=setuptools.find_packages(where='src'),
  version = '0.19',
  license='MIT',
  long_description=readme,
  long_description_content_type='text/markdown',
  description = 'Unoffical Flipper Zero cli wrapper - forked from PyFlipper',
  author = 'gabekassel',
  author_email = 'gabe@gabekassel.com',
  url = 'https://github.com/gabekassel/pyFlipper',
  project_urls={
    'Documentation': 'https://github.com/gabekassel/pyFlipper/blob/master/README.md',
    'Bug Reports':
    'https://github.com/gabekassel/pyFlipper/issues',
    'Source Code': 'https://github.com/gabekassel/pyFlipper',
  },
  keywords = ['flipper', 'wrapper', 'module'],
  install_requires=[
          'pyserial',
          'websocket-client',
      ],
  classifiers=[
    # see https://pypi.org/classifiers/
    'Development Status :: 4 - Beta',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
 ],
  python_requires='>=3.8',
)