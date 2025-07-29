from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

setup(
    name='plundergram',
    version='1.0.9',
    packages=find_packages(),
    py_modules=['Plunder'],  
    include_package_data=True,

    install_requires=[
        'telethon>=1.28.5',
        'requests>=2.25.0'
    ],

    entry_points={
        'console_scripts': [
            'plunder=PlunderGram.Plunder:main',  
        ],
    },

    author='kpwnther',
    author_email='pg.chirpy880@passmail.com',
    description='A Telegram OSINT and recon tool (for research use only).',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/kpwnther/plundergram',
    license='Apache-2.0',
    keywords='telegram osint recon cli security bot research cyber threat intelligence fraud prevention investigation phishing smishing credential harvesting',

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],

    python_requires='>=3.7',

    package_data={
        'PlunderGram': ['*.py', 'config.ini'],
        '': ['README.md', 'LICENSE'],
    }
)

