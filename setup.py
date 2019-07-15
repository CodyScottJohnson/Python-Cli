from setuptools import setup
setup(
    name = 'dbx-tableau-scraper',
    version = '0.2.0',
    install_requires=['pandas','click','numpy','tableaudocumentapi','sqlparse'],
    packages = ['dbx_tableau_scraper'],
    entry_points = {
        'console_scripts': [
            'tableau-scraper = dbx_tableau_scraper.__main__:main'
        ]
    })