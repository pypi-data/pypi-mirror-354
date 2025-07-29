# setup.py
from setuptools import setup, find_packages

# setup.py
from setuptools import setup

setup(
    name="exnummet",
    version="1.1",
    package_data={
        'exnummet': ['data/*.pdf', 'data/*.pptx'],  # явное включение файлов
    },
    include_package_data=True,  # важно для не-Python файлов
)