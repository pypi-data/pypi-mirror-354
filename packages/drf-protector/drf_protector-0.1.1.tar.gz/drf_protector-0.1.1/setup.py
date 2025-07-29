import pathlib
from setuptools import setup, find_packages # type: ignore

# Get the long description from README.md
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name='drf-protector',
    version='0.1.1',
    description='Obfuscate and package Django/DRF apps securely with PyArmor + Docker',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Pranav Dixit',
    author_email='pranavdixit20@gmail.com',
    url='https://github.com/pranav-dixit/drf-protector',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'pyarmor',
        'docker',
    ],
    entry_points='''
        [console_scripts]
        drf-protector=drf_protector.cli:main
    ''',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
