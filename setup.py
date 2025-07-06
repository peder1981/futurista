from setuptools import setup, find_packages

setup(
    name="futurista",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
        "world_bank_data",
        "pycountry",
        "plotly",
        "ipywidgets"
    ],
    author="Peder",
    author_email="seuemail@exemplo.com",
    description="Análise de dados de inflação e juros usando o Banco Mundial com visualização interativa",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/seuusuario/futurista",  # Atualize com seu repositório real
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.7",
)

