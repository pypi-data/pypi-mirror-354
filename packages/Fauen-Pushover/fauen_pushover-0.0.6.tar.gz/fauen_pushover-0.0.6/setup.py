from setuptools import setup, find_packages

setup(
        name = "Fauen-Pushover",
        version = "0.0.6",
        description = "Used for the Pushover notification service to send messages",
        author = "Daniel Bäckman",
        author_email = "daniel@backman.io",
        packages = find_packages(),
        install_requires = ["requests"],
        python_requires = ">=3.13.1",
        )
