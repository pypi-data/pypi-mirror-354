from setuptools import setup, find_packages
setup(
    name='adaptive-cards-io',
    version='1.3.4',
    author='Melqui Brito',
    author_email='melquibrito07@gmail.com',
    maintainer="Melqui Brito",
    maintainer_email="melquibrito07@gmail.com",
    description='A lightweight framework for building MS adaptive cards programmatically.',
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/melquibrito/adaptive-cards",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)