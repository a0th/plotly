from setuptools import find_packages, setup

setup(
    name="plotly-plasma",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(),
    description="A lightweight wrapper to handle some inconveniences with Plotly",
    author="Nilo Araujo",
    author_email="renard.agne@gmail.com",
    url="https://github.com/a0th/plotly",
    install_requires=["plotly>=5.0.0", "pandas>=1.0.0"],
)
