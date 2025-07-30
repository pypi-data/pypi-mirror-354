from setuptools import setup, find_packages

setup(
    name='gz7math',
    version='0.1.0',
    description='Mathematical functions for GZ7 angular system',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Zaid Emad',
    author_email='zaid.eam90@gmail.com',
    url='https://github.com/zaideam90/gz7math',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)