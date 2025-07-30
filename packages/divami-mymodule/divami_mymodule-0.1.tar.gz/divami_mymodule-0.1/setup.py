from setuptools import setup, find_packages
setup(
    name='divami_mymodule',  # Changed to a unique name
    version='0.1',
    description='A simple example module',
    author='Harshith',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'greet=divami_lib.main:greet',
            'Harshith=divami_lib.x.x:main'
        ]
    },
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)