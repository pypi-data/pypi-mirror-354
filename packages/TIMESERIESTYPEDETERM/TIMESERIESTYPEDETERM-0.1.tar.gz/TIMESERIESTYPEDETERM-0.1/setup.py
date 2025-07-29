
from setuptools import setup, find_packages


setup(name='TIMESERIESTYPEDETERM',
      version='0.1',
      description='timeseries analys',
      packages=find_packages(),
      install_requires=[
            "numpy",
            "pandas",
            "matplotlib",
            "statsmodels",
      ],
      author_email='mariapetrenko003@gmail.com',
      zip_safe=False)

