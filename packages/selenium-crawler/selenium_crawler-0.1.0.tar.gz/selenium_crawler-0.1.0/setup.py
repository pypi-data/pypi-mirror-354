from setuptools import setup, find_packages

setup(
    name="selenium-crawler",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.0.0"
    ],
    author="Jo-Hoe",
    description="Creates a simple Selenium Webdriver, optimized for web scraping.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jo-hoe/selenium-crawler",
    license="MIT",
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
