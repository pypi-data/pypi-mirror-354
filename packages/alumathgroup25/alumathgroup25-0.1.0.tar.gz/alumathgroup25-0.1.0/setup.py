from setuptools import setup, find_packages

setup(
    name="alumathgroup25",
    version="0.1.0",
    description="A friendly matrix multiplication package by Kabango Mathias.",
    author="Kabango Mathias, Orpheus Manga, Reine Mizero",
    author_email="m.kabango@alustudent.com",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    include_package_data=True,
    python_requires=">=3.6"
)
