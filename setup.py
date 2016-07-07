import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = ['pyramid', 'yosai']

setup(name='pyramid_yosai',
      version='0.0',
      description='pyramid_yosai',
      long_description='Integration of Yosai with Pyramid',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi pyramid yosai security rbac authorization',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      )
