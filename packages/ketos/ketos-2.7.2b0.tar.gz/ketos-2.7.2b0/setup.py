from setuptools import setup, find_packages
from ketos.__init__ import __version__

# create distribution and upload to pypi.org with:
#   $ python setup.py sdist bdist_wheel
#   $ twine upload dist/*

setup(name='ketos',
      version=__version__,
      description="MERIDIAN Python package for deep-learning based acoustic detectors and classifiers",
      url='https://git-dev.cs.dal.ca/meridian/ketos',
      author='Fabio Frazao, Oliver Kirsebom, Bruno Padovese',
      author_email='fsfrazao@dal.ca, oliver.kirsebom@dal.ca',
      license='GNU General Public License v3.0',
      packages=find_packages(),
      install_requires=[
          'numpy',
          'tables',
          'scipy',
          'pandas',
          'setuptools>=41.0.0',
          'tensorflow>=2.2,<=2.8',
          'scikit-learn',
          'scikit-image',
          'librosa',
          'structlog',
          'PyYAML',
          'datetime_glob',
          'matplotlib',
          'tqdm',
          'pint',
          'psutil',
          'soundfile>=0.11.0',
          'version-parser',
          'protobuf==3.20.*',
          ],
      python_requires = '>=3.10,<=3.11',
      setup_requires=['pytest-runner','wheel'],
      tests_require=['pytest', ],
      include_package_data=True,
      zip_safe=False,
      entry_points = {
        'console_scripts': [
            'ketos-run = ketos.ketos_commands.ketos_run:main',
            'ketos-metrics = ketos.ketos_commands.ketos_metrics:main',
            'ketos-train = ketos.ketos_commands.ketos_train:main',
            'ketos-create-db = ketos.ketos_commands.ketos_create_db:main'
        ]})
