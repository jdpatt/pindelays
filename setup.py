from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="pindelays",
    version="0.2.0",
    description="Excel to a Pin Delay File for either Cadence or Mentor",
    long_description=readme(),
    url="https://github.com/jdpatt/pindelays",
    author="David Patterson",
    packages=find_packages(exclude=["tests*"]),
    install_requires=["openpyxl"],
    entry_points={"console_scripts": ["pindelays = pindelays.pindelays:main"]},
    include_package_data=True,
    zip_safe=False,
)
