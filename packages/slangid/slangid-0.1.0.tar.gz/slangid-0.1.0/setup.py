from setuptools import setup, find_packages

setup(
    name="slangid",
    version="0.1.0",  # Update versi setiap release
    author="Nama Anda",
    author_email="email@anda.com",
    description="Translator slang Indonesia ↔ bahasa formal",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/syukriyansyah-ipb/slang-indonesia",
    packages=find_packages(),
    package_data={"slangid": ["data/*.json"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)