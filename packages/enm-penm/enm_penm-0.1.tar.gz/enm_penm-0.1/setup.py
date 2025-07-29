from setuptools import setup, find_packages

setup(
    name="enm-penm",
    version="0.1",
    packages=find_packages(),
    package_data={
        "numerical_methods": ["data/*.pdf"],  # включение PDF-файлов
    },
    install_requires=[       # зависимости (если есть)
        "numpy",
    ],
    author="Ваше имя",
    description="Библиотека с материалами по численным методам",
)