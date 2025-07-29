from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pymakcu",
    version="0.1.2",
    author="NeuralUser",
    author_email="admin@neuralaim.ru",
    description="Python library for controlling Makcu USB device via COM port",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NeuralAIM/pymakcu",
    
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    
    install_requires=[
        "pyserial>=3.5",
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: System :: Hardware",
        "Topic :: System :: Hardware :: Hardware Drivers",
    ],
    python_requires=">=3.7",
)