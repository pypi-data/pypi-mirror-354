from setuptools import setup, find_packages
import os

# Read README file
current_dir = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(current_dir, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = 'A Python package for converting data structures to CSV format'

setup(
    name='csv-stringify',
    version='1.0.0',
    author='Abderrahim GHAZALI',
    author_email='ghazali.abderrahim1@gmail.com',
    description='Convert Python data structures to CSV format',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/abderrahimghazali/csv-stringify',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    python_requires='>=3.7',
    install_requires=[
        # No external dependencies for core functionality
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'flake8>=3.8',
            'mypy>=0.800',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)