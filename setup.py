from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pindelays',
      version='0.1.1',
      description='Excel to a Pin Delay File for either Cadence or Mentor',
      url='https://bitbucket.org/jdpatt/pindelays/',
      author='David Patterson',
      packages=['pindelays'],
      entry_points={"console_scripts": ['pindelays = pindelays.pindelays:main']},
      include_package_data=True,
      zip_safe=False)
