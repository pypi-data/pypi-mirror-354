from setuptools import setup, find_packages

setup(
    name="alumath_matrix",
    version="0.1.0",
    author="Stecie Niyonzima",
    author_email="n.stecie@alustudent.com",
    description="A simple matrix multiplication library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Stecie06/alumath_matrix",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)