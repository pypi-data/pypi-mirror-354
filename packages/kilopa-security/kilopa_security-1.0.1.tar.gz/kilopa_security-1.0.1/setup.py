from setuptools import setup, find_packages

setup(
    name="kilopa-security",
    version="1.0.1", 
    author="Kilopa Security Team",
    author_email="security@kilopa.dev",
    description="Comprehensive Python application protection library",
    long_description="Kilopa is a comprehensive security and licensing library for Python applications with features like license management, hardware ID protection, IP monitoring, anti-tampering, and more.",
    long_description_content_type="text/plain",
    url="https://github.com/kilopa/kilopa-python",
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
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "pycryptodome>=3.15.0",
    ],
    keywords="security protection license drm anti-tamper hwid",
)
