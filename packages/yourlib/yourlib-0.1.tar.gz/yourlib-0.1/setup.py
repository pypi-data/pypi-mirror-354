from setuptools import setup, find_packages

setup(
    name='yourlib',  # must be unique on PyPI
    version='0.1',
    packages=find_packages(),
    description='My test library that prints hi',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your@email.com',
    url='https://github.com/yourname/yourlib',  # optional
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
