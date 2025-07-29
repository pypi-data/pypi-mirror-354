from setuptools import setup, find_packages

setup(
    name="simplehook",
    version="1.0.0",
    description="Simple Discord webhook wrapper",
    author="jstiin",
    url="https://github.com/jstiin/simplehook",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="discord webhook messaging",
)
