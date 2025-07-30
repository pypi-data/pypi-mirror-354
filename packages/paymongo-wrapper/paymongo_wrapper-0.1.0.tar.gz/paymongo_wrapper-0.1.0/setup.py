from setuptools import setup, find_packages

setup(
    name="paymongo-wrapper",
    version="0.1.0",
    author="Christopher I Ejada Jr",
    author_email="topeejada1@gmail.com",
    description="A simple PayMongo API wrapper for Python.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TopeMe/PaymongoWrapper",
    packages=find_packages(),
    install_requires=["requests", "python-dotenv"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={"": ["README.md", "LICENSE"]},
    keywords="paymongo payments api wrapper",
    project_urls={
        "Source": "https://github.com/TopeMe/PaymongoWrapper",
    },
)
