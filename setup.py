from setuptools import setup


setup(name='eme',
      version='5.1.0',
      description='Multi-purpose web framework',
      url='https://github.com/oboforty/eme',
      author='oboforty',
      author_email='rajmund.csombordi@hotmail.com',
      license='MIT',
      zip_safe=False,
      packages=['eme', 'eme/_tools', 'eme/_tools/commands'],
      package_data={'eme/_tools': ['content/*.tpl', 'modules/*.zip']},
      entry_points={
          'console_scripts': [
              'eme = eme._tools.cli:main',
          ],
      },
      install_requires=[
          'flask',
          'flask-login',
          'flask-mail',
          'websockets',
          'bcrypt',
          'inflect',
          'sqlalchemy',

          'authlib',
          'redis',
          'faker',
      ])
