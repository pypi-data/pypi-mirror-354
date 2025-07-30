from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="simplehook",
    version="1.4.1",
    description="Simple Discord webhook wrapper",
    long_description=long_description,  
    long_description_content_type="text/markdown", 
    author="jstiin",
    url="https://github.com/jstiin/simplehook",
    packages=find_packages(),
    install_requires=["requests", "aiofiles", "httpx"],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="discord webhook messaging",
)
