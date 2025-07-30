# setup.py

from setuptools import setup, find_packages

setup(
    name="mspro-python",
    version="0.1.0",
    description="FastAPI 项目模板初始化工具",
    author="JENA",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click"
    ],
    entry_points={
        "console_scripts": [
            "mspro-init = mspro_python.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.10",
)
