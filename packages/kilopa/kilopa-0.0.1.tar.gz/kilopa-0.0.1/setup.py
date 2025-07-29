# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kilopa",
    version="0.0.1",
    author="AmKilopa",
    author_email="yurybaltsev@gmail.com",
    description="🛡️ Невидимая система защиты Python приложений с демо-периодом",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AmKilopa/kilopadev",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "flask>=2.0.0",
        "flask-cors>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "kilopa-admin=kilopa.admin_server:main",
        ],
    },
    keywords="protection license demo security drm trial python",
    project_urls={
        "Bug Reports": "https://github.com/AmKilopa/kilopadev/issues",
        "Source": "https://github.com/AmKilopa/kilopadev",
    },
)