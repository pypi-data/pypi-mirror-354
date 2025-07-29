from setuptools import setup, find_packages

setup(
    name = "data-pipeline-helper-krishna",
    version='0.1.0',
    author='Mohana Krishnan N',
    author_email='mohankrishnan1404@gmail.com',
    description='A helper library for building and managing data pipelines',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/username/data-pipeline-helper',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas',
        'boto3'
    ]
)