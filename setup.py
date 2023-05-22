from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str) -> List[str]:
    """Returns a list of requirements read from a file.
    
    This function reads a file containing a list of requirements, with each requirement on a separate line. 
    It removes any newline characters and returns a list of cleaned requirements.

    Args:
        file_path (str): The path to the file containing the requirements.

    Returns:
        List[str]: A list of requirements.
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