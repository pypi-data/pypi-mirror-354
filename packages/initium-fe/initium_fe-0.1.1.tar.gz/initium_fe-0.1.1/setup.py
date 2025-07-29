from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="initium-fe",
    version="0.1.1",
    author="Sahil Jasani",
    author_email="jasanisahil11@gmail.com",
    description="Project Bootstrap Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/autowerk/initium",
    packages=find_packages(),
    package_data={
        'initium': ['templates/**/*'],
    },
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'initium=initium.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
) 