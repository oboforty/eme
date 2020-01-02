from setuptools import setup

setup(name='eme',
      version='4.9.0',
      description='Multi-purpose web framework',
      url='https://github.com/oboforty/eme',
      author='oboforty',
      author_email='rajmund.csombordi@hotmail.com',
      license='MIT',
      zip_safe=False,
      packages=['eme', 'eme/vendor', 'eme/auth'],
      entry_points={
          'console_scripts': [
              'eti = snek:main',
          ],
      },
      install_requires=[
          'flask',
          'flask-login',
          'flask-mail',
          'bcrypt',

          'sqlalchemy',
          'redis',
          'faker',
      ])
