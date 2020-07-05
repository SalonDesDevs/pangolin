import setuptools

with open("README.md", "r") as fd:
    long_description = fd.read()

with open("VERSION", "r") as fd:
    version = fd.read().strip()

setuptools.setup(
    name="pangolin",
    version=version,
    author="Thomas Marchand, Julien Castiaux, Antoine Tournepiche, Charlotte Thomas",
    author_email="julien.castiaux@gmail.com",
    description="A game about bubbles and a 10s timer ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SalonDesDevs/pangolin",
    packages=setuptools.find_packages(),
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
    ],
)
