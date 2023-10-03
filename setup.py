from setuptools import setup, find_packages

setup(
    name='notion_db_integration',
    version='0.1.0',
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