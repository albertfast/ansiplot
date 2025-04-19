from setuptools import setup, find_packages

setup(
    name='ansiplot',
    version='0.1.3+ahmet',
    description='Terminal plotting with vertical histogram and bar chart labels by Ahmet Sahiner',
    author='Ahmet Sahiner',
    author_email='ahmethasimsahiner@icloud.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)

