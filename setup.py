from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str) -> List[str]:
    """Returns a list of requirements.

    Args:
        file_path (str): _description_

    Returns:
        List[str]: _description_
    """
    requirements = []

    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [requirement.replace('\n', '') for requirement in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements

setup(
    name='bike-availability-prediction',
    version='1.0',
    author='Javier De la Ossa',
    author_email='javdelfer@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)