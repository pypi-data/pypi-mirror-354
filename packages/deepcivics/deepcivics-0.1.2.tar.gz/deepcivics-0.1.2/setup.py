from setuptools import setup, find_packages

setup(
    name="deepcivics",
    version="0.1.2",
    author="Pkbythebay29",
    author_email="kannan@haztechrisk.org",
    description="Opensource, LLM powered library to turn public data into civic insight for the Public, Policy makers and Investment professionals.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pkbythebay29/deepcivics",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pandas", "matplotlib", "transformers", "pyyaml"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)