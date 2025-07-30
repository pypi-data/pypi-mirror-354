from setuptools import setup, find_packages

setup(
    name="osonkod",
    version="0.1.0",
    description="O'zbek tilida yozilgan dasturlash tili",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="nbbdev",
    author_email="nabiyevbahrom258@gmail.com",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
)
