from setuptools import setup, find_packages

setup(
    name="easy_kivy_engine",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "kivy>=2.3.1",
    ],
    author="Yiqian Gao",
    author_email="janiago.jerry@gmail.com",
    description="A Kivy-based game engine",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/janiago/easy_kivy_engine",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)