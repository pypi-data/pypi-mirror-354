from setuptools import setup, find_packages

setup(
    name="fluentc-sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    author="FluentC",
    author_email="support@fluentc.io",
    description="Python SDK for FluentC Translation API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FluentC/python-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.7",
)