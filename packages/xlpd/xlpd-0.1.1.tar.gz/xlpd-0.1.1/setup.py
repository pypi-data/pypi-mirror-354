from setuptools import setup, find_packages

setup(
    name="xlpd",
    version="0.1.1",
    author="Yinchu Xia",
    author_email="sales@pytorchsoft.com",
    description="xiu lian ping de",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pytorchsoft/xlpd",
    packages=find_packages(),
    install_requires=[
        "numpy",  # List your dependencies here
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "xlpd = cli:main",
        ]
    },
)
