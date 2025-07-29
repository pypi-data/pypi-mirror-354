from setuptools import setup, find_packages
import os


# Read README file for long description
def read_readme():
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    return ("A Python package for accessing the HATS (Hindi Analogy Test Set) "
            "dataset with controlled access")


setup(
    name="hats-analogy-dataset",
    version="1.0.0",
    author="Ashray Gupta, Rohan Joseph, Sunny Rai",
    author_email="rohan18545@mechyd.ac.in",
    description=(
        "HATS: Hindi Analogy Test Set - A controlled access package for "
        "evaluating reasoning in Large Language Models"
    ),
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Inequilazitive/HATS-Hindi_Analogy_Test_Set",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
    ],
    include_package_data=True,
    package_data={
        "analogy_dataset": ["data/*.csv"],
    },
    keywords=("analogy, dataset, hindi, nlp, machine learning, "
              "llm evaluation, reasoning, controlled access, test set, "
              "research"),
    project_urls={
        "Bug Reports": (
            "https://github.com/Inequilazitive/"
            "HATS-Hindi_Analogy_Test_Set/issues"
        ),
        "Source": (
            "https://github.com/Inequilazitive/HATS-Hindi_Analogy_Test_Set"
        ),
        "Documentation": (
            "https://github.com/Inequilazitive/"
            "HATS-Hindi_Analogy_Test_Set/blob/main/README.md"
        ),
        "Research Paper": "https://aclanthology.org/",
    },
) 