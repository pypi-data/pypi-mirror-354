from setuptools import setup, find_packages

setup(    name="skytup",
    version="0.1.1",
    packages=find_packages(),
    install_requires=["click>=8.0.0"],
    author="Skytup",
    author_email="skytup91@gmail.com",
    description="A sample Python package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/skytup/pypi.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'skytup=skytup:cli',
        ],
    },
)