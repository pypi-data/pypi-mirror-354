from setuptools import setup, find_packages

setup(
    name="saranglebah",
    version="0.1.0",
    description="Broadcast keystrokes from a master PC to multiple slaves over Wi‑Fi",
    author="",
    packages=find_packages(),
    install_requires=["pynput>=1.7"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "saranglebah=saranglebah.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
