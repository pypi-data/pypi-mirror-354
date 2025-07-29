from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fumes",
    version="0.1.0",
    author="Taizun",
    author_email="taizun8@gmail.com",
    description="A Python library for building web-based AI/data apps with custom frontends",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/t4zn/fumes",
    project_urls={
        "Bug Tracker": "https://github.com/t4zn/fumes/issues",
        "Documentation": "https://github.com/t4zn/fumes#readme",
        "Source Code": "https://github.com/t4zn/fumes",
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "websockets>=10.0",
        "python-multipart>=0.0.5",
        "jinja2>=3.0.0",
        "watchdog>=2.1.0",
        "click>=8.0.0",
        "pydantic>=1.8.0",
        "aiofiles>=0.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "isort>=5.0",
            "mypy>=0.910",
            "build>=0.7.0",
            "twine>=3.4.2",
        ]
    },
    entry_points={
        "console_scripts": [
            "fumes=fumes.cli.main:cli",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: FastAPI",
    ],
    python_requires=">=3.8",
    keywords="web,ai,data,ui,framework,streamlit,gradio",
)