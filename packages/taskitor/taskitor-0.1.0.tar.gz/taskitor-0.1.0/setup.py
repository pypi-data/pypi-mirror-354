from setuptools import setup, find_packages

setup(
    name="taskitor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["rich"],
    entry_points={
        "console_scripts": [
            "taskitor=taskitor.main:main",
        ]
    },
    author="Aitor",
    description="A simple task tracker CLI using Python and Rich.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PyTorDev/taskitor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)