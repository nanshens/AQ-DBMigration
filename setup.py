from setuptools import setup, find_packages

setup(
    name="aq_dbmigration",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[
        "psycopg2>=2.9.9",
        "mysql-connector-python>=9.0.0",
        "uuid>=1.30",
        "loguru>=0.7.2"
    ],
    author="nanshens",
    author_email="619232906@qq.com",
    description="a database migration tool",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/nanshens/AQ-DBMigration",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
