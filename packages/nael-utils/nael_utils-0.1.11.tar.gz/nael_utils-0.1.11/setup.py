from setuptools import setup, find_packages

setup(
    name="nael-utils",
    version="0.1.11",
    description="A collection of utilities for Python.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Nael",
    author_email="nael.nathanael71@gmail.com",
    url="https://github.com/Nael-Nathanael/nael-utils",
    packages=find_packages(),
    package_data={
        "nael_utils": ["py.typed"],
    },
    install_requires=[
        "langchain-core",
        "langchain-openai",
        "langchain-anthropic",
        "openai",
        "pydantic",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    python_requires='>=3.9',
    zip_safe=False,
)
