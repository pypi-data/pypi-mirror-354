from setuptools import setup, find_packages

setup(
    name='skyto',
    version='0.4',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'skyto=skyto.cli:main',
        ],
    },
    author='Lanscky Tshinkola',
    description='Skyto est un langage de programmation pédagogique basé sur Python, permettant d’écrire du code en Lingala et faire de l’intelligence artificielle',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
