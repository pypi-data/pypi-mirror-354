from setuptools import setup, find_packages

setup(
    name="gokulsmodule",
    version="0.1.3",
    author="NT Gokul",
    author_email="gokulnt2008@gmail.com",
    description="Module has a lot of cool stuff in it :DDD",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TheGlork/GokulsModule",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
