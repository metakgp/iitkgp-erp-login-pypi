from setuptools import setup, find_packages

setup(
    name='iitkgperp',
    version='0.1',
    description='A module to automate the login process of ERP at IIT-KGP',
    author='Arpit Bhardwaj',
    author_email='proffapt@pm.me',
    url='https://github.com/proffapt/iitkgp-erp-pypi',
    packages=find_packages(),
    install_requires=[
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client',
        'requests',
        'bs4',
    ],
)
