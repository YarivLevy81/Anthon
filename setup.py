from setuptools import setup, find_packages

setup(
    name = 'Anton',
    version = '1.0.1',
    author = 'Yariv Levy',
    description = 'Final project at Advanced System Design course at TAU',
    packages = find_packages(),
    tests_require = ['pytest', 'pytest-cov'],
)