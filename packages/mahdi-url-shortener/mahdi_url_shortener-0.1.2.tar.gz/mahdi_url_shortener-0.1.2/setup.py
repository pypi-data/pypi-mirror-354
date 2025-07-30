import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mahdi-url-shortener",
    version="0.1.2",
    author="oxl_mahdi",
    author_email="mhasan37608@gmail.com",
    description="A simple Python package to shorten URLs via TinyURL with CLI support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oxl_mahdi/mahdi-url-shortener", 
    project_urls={
        "Bug Tracker": "https://github.com/oxl_mahdi/mahdi-url-shortener/issues",
        "Source": "https://github.com/oxl_mahdi/mahdi-url-shortener",
    },
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "pyshorteners>=1.0.1",
    ],
    entry_points={
        "console_scripts": [
            "mahdi=mahdi.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Environment :: Console",
    ],
    license="MIT",
)
