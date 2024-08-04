from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        # Remove comments and empty lines
        lines = [line for line in lines if line and not line.startswith("#")]
    return lines


setup(
    name="llm-labeller",
    version="0.1.0",
    description="A package for leveraging LLMS for dataset creation",
    # long_description=open("README.md").read(),
    # long_description_content_type="text/markdown",
    author="Graeon Bergen",
    author_email="graesonbergen@gmail.com",
    url="https://github.com/GraesonB/llm-labeller",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=parse_requirements("requirements.txt"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
