from setuptools import setup, find_packages

setup(
    name="tongban_report",
    version="0.2.7",
    author="liwenhuan",
    author_email="liwh@tongbaninfor.com",
    license = "MIT AND (Apache-2.0 OR BSD-2-Clause)",
    description="A short description of your package",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="http://192.168.2.252:9980/tongban-qa/tongban_report.git",
    packages=find_packages(),
    package_data={
        "tongban_report": ["assets/*.png"]
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "python-docx",
        "matplotlib",
        "openpyxl"
    ],
    entry_points={
        "console_scripts": [
            "tongban_report=tongban_report.main:main",
        ],
    },
)