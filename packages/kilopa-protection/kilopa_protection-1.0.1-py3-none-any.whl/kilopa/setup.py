# Создайте файл setup.py в D:\Project\Kilopa-PIP\setup.py

from setuptools import setup, find_packages

setup(
    name="kilopa",
    version="1.0.0",
    author="Kilopa Security",
    author_email="security@kilopa.dev",
    description="Библиотека защиты Python-приложений",
    long_description="Kilopa - комплексная система защиты для Python-приложений",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "pycryptodome>=3.15.0",
    ],
    zip_safe=False,
)