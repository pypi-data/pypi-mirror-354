from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")


setup(
    name='muhidinlib',  # Ganti dengan nama pustaka kamu
    version='0.1.1',
    description='"Utility Python sederhana yang sering digunakan dalam proyek data science."',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Asep Muhidin',
    author_email='asep.muhidin@pelitabangsa.ac.id',
    url='https://github.com/asepmuhidin',  # Opsional
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'seaborn',
        'numpy',
        'scipy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)