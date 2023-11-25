from setuptools import find_packages, setup

setup(
    name="plotly-plasma",
    version="0.2.1",
    packages=find_packages(),
    description="A small opinionated enhancement for Plotly",
    author="Nilo Araujo",
    author_email="renard.agne@gmail.com",
    url="https://github.com/a0th/plotly",
    install_requires=["plotly>=5.0.0", "pandas>=1.0.0"],
)
