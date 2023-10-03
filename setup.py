from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "Readme.md").read_text()

setup(
    name='notion_db_integration',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.1',
    author='Arjun',
    author_email='arjunprakash027@gmail.com',
    description='A wrapper around Notion API to perform CRUD operations on your notion database',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)