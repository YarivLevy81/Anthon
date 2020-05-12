from setuptools import setup, find_packages

setup(
    name = 'Anthon',
    version = '1.0.0',
    author = 'Yariv Levy',
    description = 'Final project at Advanced System Design course at TAU',
    packages = find_packages(),
    tests_require = ['pytest', 'pytest-cov'],
)