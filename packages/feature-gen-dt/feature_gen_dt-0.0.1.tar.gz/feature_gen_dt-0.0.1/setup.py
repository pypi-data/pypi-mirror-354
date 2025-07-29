from setuptools import setup

setup(
    name="feature_gen_dt",
    version="0.0.1",
    author="cdh@wearehackerone.com",
    author_email="cdh@wearehackerone.com",
    description="Telemetry research package for dependency analysis.",
    long_description="This package is used for research purposes to detect dependency loading.",
    long_description_content_type="text/markdown",
    url="https://hackerone.com/cdh",
    packages=["feature_gen_dt"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
