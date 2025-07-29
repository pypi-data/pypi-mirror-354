from setuptools import setup, find_packages

setup(
    name="pygame_framework_1just_josh",
    version="0.0.2",
    author="Joshua - jjboy2245",
    description="this is a simple pygame wrapper for advanced game features with less boilerplate",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)