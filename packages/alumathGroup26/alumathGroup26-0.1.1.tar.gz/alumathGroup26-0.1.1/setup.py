from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="alumathGroup26",
    version="0.1.1",
    author="Terry Manzi",
    author_email="m.terry@alustudent.com",
    description="A simple matrix calculator library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lGikundiro/Advanced-Linear-Algebra---Formative-2",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[],
    keywords="matrix, mathematics, linear algebra, calculator",
)