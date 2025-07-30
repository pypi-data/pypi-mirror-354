from setuptools import setup, find_packages

setup(
    name="sicoob-sdk",
    version="0.1.3",
    description="SDK Python para integração com a API do Banco Sicoob",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="Fábio Thomaz",
    author_email="fabio@ladder.dev.br",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "python-dotenv>=0.15.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
