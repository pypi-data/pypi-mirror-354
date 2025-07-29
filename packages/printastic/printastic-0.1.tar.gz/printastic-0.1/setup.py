from setuptools import setup, find_packages

setup(
    name="printastic",
    version="0.1",
    packages=find_packages(),
    install_requires=["rich"],
    author="Anuj Thapa",
    description="A pretty fantastic terminal output formatter",
)
