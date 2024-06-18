"""
Setup Tool for Global Custom Utilities.
"""

from setuptools import setup, find_packages

setup(
    name='utils',
    version='0.0.1',
    author='me',
    author_email='...',
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['tests', 'test_*.py']),
    zip_safe=False,
    install_requires=[
        'assertpy==1.1',  # Used in my_utils.common_assertions
        'python-decouple==3.8',  # Used to get environment variables
        'pytest==7.4.0',  # Used to get pytest environments
        'requests==2.31.0',  # Used to send requests
        'pytest-ordering==0.6'

    ],
    python_requires='==3.10.6'
)

# To run the tests, follow the instructions below:
# 1. Create an environment inside global_utils/src
# 2. Activate the environment
# 3. Install requirements.txt from the project root directory
# 4. Install the global_utils
# 5. Go inside global_utils/src/tests
# 6. Run unittest command: python -m unittest
