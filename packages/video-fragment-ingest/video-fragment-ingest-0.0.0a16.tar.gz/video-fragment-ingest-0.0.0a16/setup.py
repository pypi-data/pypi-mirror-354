from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="video-fragment-ingest",
    include_package_data=True,
    python_requires='>=3.10',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    setup_requires=['setuptools-git-versioning'],
    install_requires=requirements,
    author="Andres Godoy",
    author_email="andres@volt.ai",
    description="Kafka-based ingest and decoding classes for VideoIngestFragments",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setuptools_git_versioning={
        "enabled": True,
        "dirty_template": "{tag}",
    }
)
