from setuptools import setup, find_packages

setup(
    name="pyinternals",  # your package name on PyPI
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    author="Mohamed Desouky",
    author_email="Mohamed.d180@gmail.com",
    description="A visualizer for Python object layout in CPython",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cpy_layouts",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # or whatever license you use
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
