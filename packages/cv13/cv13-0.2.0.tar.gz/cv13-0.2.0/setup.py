from setuptools import setup, find_packages

setup(
    name="cv13",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "pyperclip>=1.8.2",
        "openai>=1.84.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
