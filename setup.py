from setuptools import setup, find_packages

setup(
    name = 'FinalProject',
    version = '0.1.0',
    author = 'Yariv Levy',
    description = 'Final project at Advanced System Design course at TAU',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest', 'pytest-cov'],
)