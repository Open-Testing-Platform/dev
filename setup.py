from setuptools import setup

setup(
    name="dev",
    version="0.1.0",
    py_modules=["dev"],
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "dev = dev:app",
        ],
    },
)
