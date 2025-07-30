from setuptools import setup, find_packages

setup(
    name="xlpd",
    version="0.1.9",
    author="Yinchu Xia",
    author_email="sales@pytorchsoft.com",
    description="Xiu Lian Pin De",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pytorchsoft/xlpd",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[],
    classifiers=[],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "xlpd = xlpd.cli:app",
        ]
    },
)
