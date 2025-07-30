from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="authfi-api",
    version="0.0.3",
    author="chumicat",
    author_email="russell57260620@gmail.com",
    description="Python wrapper for Authentrend AuthFi WebAuthn/FIDO2 API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chumicat/authfi-api",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security :: Cryptography",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="webauthn fido2 authentication authfi authentrend security",
    project_urls={
        "Bug Reports": "https://github.com/chumicat/authfi-api/issues",
        "Source": "https://github.com/chumicat/authfi-api",
        "Documentation": "https://github.com/chumicat/authfi-api#readme",
    },
)