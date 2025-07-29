# setup.py

from setuptools import setup, find_packages
from pathlib import Path

dir = Path(__file__).parent
long_description = (dir / "README.md").read_text()


setup(
    name='kbomodels',
    version='2025.1.0',
    author='Abdullahi Kabir Bindawa',
    author_email='ka.bindawa@gmail.com; kabir.abdullahi.ng@gmail.com',
    description='A Python package for Kabirian-based optinalysis (KBO) and other advanced estimations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['numpy'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)

# FOR PACKAGING
# python setup.py bdist_wheel

# FOR LOCAL INSTALLATION
# pip install dist/kbomodels-2025.1.0-py3-none-any.whl

# FOR TESTING
# pip install --index-url https://test.pypi.org/simple/ my_package
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# FOR UPLOAD TO PUBLIC REPOSITORY
# pip install twine
# twine upload dist/*

# Test: U & P = bindawa, Kabir@test*
# original: U & P = optinalysis, Kabir@kbomodels*
