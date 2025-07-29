from setuptools import setup, find_packages

setup(
    name='cyrillecv',
    version='1.0.0',
    description='CV interactif de Cyrille Gbale',
    author='Cyrille Gbale',
    author_email='crvgbale@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cyrillecv=cyrillecv.main:main',
        ],
    },
    install_requires=[
        'rich',
    ],
)
