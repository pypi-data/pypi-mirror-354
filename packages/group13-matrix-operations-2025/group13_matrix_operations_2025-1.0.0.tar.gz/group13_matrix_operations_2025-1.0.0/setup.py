from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="group13-matrix-operations-2025",
    version="1.0.0",
    author="Group13",
    author_email="e.twizeyima@alustudent.com",
    description="Advanced Linear Algebra Matrix Operations for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/twizelissa/alugroup13-library.git",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=6.0", "black", "flake8"],
    },
    keywords="linear algebra, matrix, multiplication, mathematics, numpy",
    project_urls={
        "Bug Reports": "https://github.com/twizelissa/alugroup13-library.gitissues",
        "Source": "https://github.com/twizelissa/alugroup13-library.gitalumathgroup13",
    },
)
