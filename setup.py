from setuptools import find_packages, setup
setup(
    name='sssyntax',
    packages=find_packages(include=['sssyntax']),
    version='0.1.0',
    description='Super Simple Syntax',
    author='robert.kenneth.smart@gmail.com',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)