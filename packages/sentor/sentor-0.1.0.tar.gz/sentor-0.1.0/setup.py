from setuptools import setup, find_packages

setup(
    name="sentor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "sentor=sentor.client:main",
        ],
    },
)