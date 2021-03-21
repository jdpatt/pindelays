from setuptools import find_packages, setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="pindelays",
    version="1.0.0",
    description="Excel to a Pin Delay File for either Cadence or Mentor",
    long_description=readme(),
    url="https://github.com/jdpatt/pindelays",
    author="David Patterson",
    packages=find_packages(exclude=["tests*"]),
    install_requires=["click", "openpyxl"],
    entry_points={"console_scripts": ["pindelays = pindelays.pindelays:pindelay"]},
    include_package_data=True,
    zip_safe=False,
)
