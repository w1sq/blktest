from setuptools import setup, find_packages

setup(
    name="blktest",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "py-gnuplot",
    ],
    entry_points={
        "console_scripts": [
            "blktest=src.blktest:main",
        ],
    },
    author="Kokorev Artem",
    author_email="artem.kokorev2005@yandex.ru",
    description="Block device performance testing utility",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/w1sq/blktest",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
