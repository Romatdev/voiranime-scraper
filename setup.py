from setuptools import setup

setup(name='voiranime',
      version='0.1',
      description='Voiranime scrap service by Cwazy#8385',
      author='Cwazy#8385',
      author_email='cwazydev@gmail.com',
      packages=['voiranime'],
      install_requires=[
          'requests',
          'beautifulsoup4',
      ])