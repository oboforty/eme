from setuptools import setup


setup(name='eme',
      version='1.5.1.4',
      description='Multi-purpose web framework',
      url='https://github.com/oboforty/eme',
      author='oboforty',
      author_email='rajmund.csombordi@hotmail.com',
      license='MIT',
      zip_safe=False,
      packages=['eme', 'eme/vendor', 'eme/auth', 'eme_tools', 'eme_tools/commands'],
      package_data={'eme_tools': ['content/*.tpl', 'content/*.zip']},
      entry_points={
          'console_scripts': [
              'eme = eme_tools.cli:main',
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
          'inflect'
      ])
