from setuptools import setup, find_packages

setup(
    name="dsl_modulo",
    version="0.1.1",
    description="A module that contains functions designed extract and organize legal data, especially in Brazilian courts.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(include=['dsl_modulo', 'dsl_modulo.*']),
    package_dir={'': '.'},
    package_data={
        'dsl_modulo': ['*.py', '*.md', 'LICENSE'],
    },
    install_requires=[
        'requests>=2.25.1',
        'selenium>=4.0.0',
    ],
    python_requires=">=3.6",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)