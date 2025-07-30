from setuptools import setup, find_packages

setup(
    name="dsl_functions",
    version="1.3.0",
    description="A module that contains functions designed extract and organize legal data, especially in Brazilian courts.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Alexandre Araújo Costa",
    author_email="alexandre.araujo.costa@gmail.com",
    packages=find_packages(include=['dsl_functions', 'dsl_functions.*']),
    package_dir={'': '.'},
    package_data={
        'dsl_functions': ['*.py', '*.md', 'LICENSE'],
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