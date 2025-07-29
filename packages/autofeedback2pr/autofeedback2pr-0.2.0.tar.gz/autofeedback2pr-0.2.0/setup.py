from setuptools import setup, find_packages

setup(
    name="autofeedback2pr",
    version="0.2.0",
    description="Auto feedback classifier and grader for developer workflow.",
    author="ITworkonline",
    author_email="jay123.studio@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    python_requires=">=3.7",
    url="https://github.com/ITworkonline/autofeedback2pr",
    license="MIT",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
) 