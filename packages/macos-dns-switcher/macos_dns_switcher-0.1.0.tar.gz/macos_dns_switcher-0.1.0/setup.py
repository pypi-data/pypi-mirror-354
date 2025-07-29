from setuptools import setup, find_packages

setup(
    name="macos-dns-switcher",
    version="0.1.0",
    description="CLI tool to switch DNS providers for macOS network services",
    author="JimmyMtl",
    author_email="j.mtlk.pro@outlook.fr",
    url="https://github.com/JimmyMtl/macos-dns-switcher",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "mdns = mdns.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ],
)
