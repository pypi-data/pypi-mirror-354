from setuptools import setup, find_packages

setup(
    name="cv_gg",  # Название библиотеки
    version="0.1.0",  # Версия
    packages=find_packages(),
    include_package_data=True,  # Включаем package_data
    package_data={"cv_gg": ["data/all_CV.txt"]},  # Указываем файлы данных
    install_requires=[],  # Укажи зависимости, если есть
    description="ACV - скат по задачам",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
