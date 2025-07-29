from setuptools import setup, find_packages

setup(
    name="nanosignfs",
    version="0.1.1",
    author="Raghava Chellu",
    author_email="raghava.chellu@gmail.com",
    description="A Linux FUSE filesystem that signs files on write using GPG (PKI), ideal for nano-data pipelines.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nanosignfs",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fusepy",
        "python-gnupg"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
        "Topic :: Security :: Cryptography",
        "Topic :: System :: Filesystems",
    ],
    python_requires=">=3.7",

    # Add your keywords here
    keywords=[
        "fuse",
        "gpg",
        "filesystem",
        "cryptography",
        "signing",
        "pki",
        "nano-data",
        "virtual filesystem",
        "python-fuse",
        "linux-filesystem"
    ],
)

