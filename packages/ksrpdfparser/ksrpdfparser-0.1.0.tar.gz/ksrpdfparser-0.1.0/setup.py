from setuptools import setup, find_packages
setup(
    name="ksrpdfparser",
    version="0.1.0",
    description="Extract text, images, tables, and layout from PDF files using PyMuPDF and pdfplumber.",
    author="Siva Reddy Kanala",
    author_email="ksr199221@gmail.com",
    packages=find_packages(),
    install_requires=["pymupdf>=1.22.0", "pdfplumber>=0.9.0"],
    include_package_data=True,
    python_requires=">=3.7",
)
