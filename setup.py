import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

requirements = ["pop>=12", "aiohttp>=3.6.2", "GitPython>=3.1.1"]
dev_requirements = []

setuptools.setup(
    name="metarepo_cpe_tag",
    version="1.0.0",
    author="mrl5",
    description="Tool for tagging Funtoo meta-repo with CPEs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrl5/metarepo-cpe-tag",
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={"dev": dev_requirements},
    packages=setuptools.find_packages(),
)
