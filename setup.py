# setup.py

from setuptools import setup, find_packages

setup(
    name='cheerlights_api',
    version='0.1.1',
    description='A Python package to interact with the CheerLights API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Hans Scharler',
    author_email='hscharler@gmail.com',
    url='https://github.com/cheerlights/cheerlights-python-package',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)