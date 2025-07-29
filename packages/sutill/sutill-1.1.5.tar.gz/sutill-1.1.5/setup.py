from setuptools import setup, find_packages

setup(
    name="sutill",
    version="1.1.5",
    packages=find_packages(),
    package_data={
        "diffusers_helper": ["*.so"],
    },
    include_package_data=True,
    author="HuggingFace",
    description="Python wrapper around a shared library",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
