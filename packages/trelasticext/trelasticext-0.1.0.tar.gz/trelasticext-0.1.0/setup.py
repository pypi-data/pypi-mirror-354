from setuptools import setup, find_packages

setup(
    name="trelasticext",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "elasticsearch>=8.0.0,<9.0.0",
        "pandas",
        "numpy",
    ],
    python_requires=">=3.6",
    url="https://github.com/millerhadar/trelasticext",
    project_urls={
        "Bug Tracker": "https://github.com/millerhadar/trelasticext/issues",
        "Documentation": "https://github.com/millerhadar/trelasticext",
        "Source Code": "https://github.com/millerhadar/trelasticext",
    },
)