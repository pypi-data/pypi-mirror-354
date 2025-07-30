from setuptools import find_packages, setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='speedsense',
    packages=find_packages(include=['speedsense']),
    version='0.1.2',
    description='Time complexity analyser',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Anant Terkar',
    url="https://github.com/anantterkar/SpeedSense",
    author_email="20bcs014@iiitdwd.ac.in",
    license="MIT",
    install_requires=['matplotlib>=3.10.1', "numpy>=2.2.5"],
    extras_require={
        "dev": ["pytest>=8.3.5", "twine>=6.1.0"]
    }
)
