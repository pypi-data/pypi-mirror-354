from setuptools import setup, find_packages

setup(
    name="Mal-Detector",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "rich",
        "jinja2"
    ],
    entry_points={
        'console_scripts': [
            'vt-scan=vt_scan.__main__:main'
        ]
    },
    author="Bismoy Ghosh",
    description="VirusTotal CLI scanner for files and URLs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
