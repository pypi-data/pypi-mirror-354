from setuptools import setup,find_namespace_packages
from os import listdir
setup(name='somper',
      version='1.0',
      url='https://github.com',
      license='MIT',
      author='Levap Vobayr',
      author_email='pppf@hmail.ri',
      description='',
      packages=find_namespace_packages(where="src"),
      package_dir={"": "src"},
      package_data={},
      zip_safe=False)
