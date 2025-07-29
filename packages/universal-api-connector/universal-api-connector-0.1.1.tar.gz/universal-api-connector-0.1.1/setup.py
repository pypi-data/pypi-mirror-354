from setuptools import setup, find_packages

setup(
    name="universal-api-connector",
    version="0.1.1",
    description="Universal OpenAPI-driven API connector",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "requests",
        "PyYAML",
        "streamlit",
        "requests_oauthlib"
    ],
    python_requires=">=3.7",
    include_package_data=True,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/universal-api-connector",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
