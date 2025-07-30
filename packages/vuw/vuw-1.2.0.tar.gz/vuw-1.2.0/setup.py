from setuptools import setup, find_packages

setup(
    name="vuw",
    version="1.2.0",
    description="A Python package for demonstration",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Jiwon Chae",
    author_email="jwchae106@gmail.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.1",
        "numpy>=1.21.6",
        "joblib>=1.3.2",
        "pandas>=1.1.5",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
)

