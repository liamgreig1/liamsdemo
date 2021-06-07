from setuptools import setup, find_packages

requirements = [
    "boto3~=1.17.79",
    "fastapi~=0.65.1",
    "sentry-sdk~=1.1.0",
    "watchtower~=1.0.6",
]

dev_requirements = [
    "black~=21.5b0",
    "coverage~=5.5",
    "flake8~=3.9.2",
    "pytest~=6.2.4",
    "requests~=2.25.1",
    "uvicorn~=0.13.4",
]

setup(
    name="liamsdemo",
    version="0.1.0",
    packages=find_packages(include=["app.*"]),
    install_requires=requirements,
    extras_require={"dev": dev_requirements},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ]
)
