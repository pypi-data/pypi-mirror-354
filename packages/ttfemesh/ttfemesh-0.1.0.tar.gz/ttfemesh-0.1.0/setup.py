from setuptools import setup, find_packages

ascii_logo = """
████████╗████████╗███████╗███████╗███╗   ███╗
╚══██╔══╝╚══██╔══╝██╔════╝██╔════╝████╗ ████║ 
   ██║      ██║   █████╗  █████╗  ██╔████╔██║ 
   ██║      ██║   ██╔══╝  ██╔══╝  ██║╚██╔╝██║ 
   ██║      ██║   ██║     ███████╗██║ ╚═╝ ██║ 
   ╚═╝      ╚═╝   ╚═╝     ╚══════╝╚═╝     ╚═╝ 
"""

print(ascii_logo)

requirements = [
    requirement.strip() for requirement in open('requirements.txt').readlines()
]

setup(
    name="ttfemesh",
    version="0.1.0",
    description="A Python library for tensor train-based finite element meshing.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mazen Ali",
    author_email="mazen.ali90@gmail.com",
    url="https://github.com/MazenAli/tt-femesh",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.9, <3.13",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries",
    ],
    project_urls={
        "Source": "https://github.com/MazenAli/tt-femesh",
        "Documentation": "https://github.com/MazenAli/tt-femesh",
    },
    keywords="tensor train finite elements meshing simulation",
)
