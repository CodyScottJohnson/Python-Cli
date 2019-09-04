from setuptools import setup
setup(
    name = 'cli_name',
    version = '0.2.0',
    install_requires=['click'],
    packages = ['cli_name'],
    entry_points = {
        'console_scripts': [
            'cli_name = cli_name.__main__:main'
        ]
    })