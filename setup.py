from setuptools import setup, find_packages

setup(
    name='wexample-helpers-app',
    version=open('version.txt').read(),
    author='weeger',
    author_email='contact@wexample.com',
    description='Helpers for building Python app or cli.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wexample/python-helpers-app',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'pydantic',
        'wexample-helpers',
    ],
    python_requires='>=3.6',
)
