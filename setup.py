import os
from setuptools import setup, find_packages, Command

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info; py.cleanup -d')


here = os.path.abspath(os.path.dirname(__file__))

requires = ['pyramid', 'yosai']

setup(name='pyramid_yosai',
      version='0.1.0',
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
      cmdclass={'clean': CleanCommand}
      )
