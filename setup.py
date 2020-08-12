import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py591",
    version="0.0.2",
    author="Frank Chang",
    author_email="frank@csie.io",
    description="Parser and parsing API service for 591 Housing Rental service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frankurcrazy/591HousingApi",
    packages=setuptools.find_packages(),
    license="BSD",
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet",
    ],
    keywords=["api", "591", "housing"],
    python_requires='>=2.7,>=3.5',
    install_requires=[
        "beautifulsoup4==4.9.1",
        "Flask==1.1.2",
        "Pillow==7.2.0",
        "pytesseract==0.3.5",
        "requests==2.24.0",
    ]
)
