from setuptools import setup, find_packages

setup(
    name="taskli",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "typer",
        "rich"
    ],
    entry_points={
        'console_scripts': [
            'taskli=taskli.cli:app',
        ],
    },
)