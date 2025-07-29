from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='thallu',
    version='0.1.7',
    author='Naveensivam03',
    description='Lightweight CLI to streamline Git workflows',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Naveensivam03/thallu',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Version Control :: Git',
    ],
    python_requires='>=3.7',
    install_requires=[
        "inquirer>=3.4.0",
        "questionary>=2.1.0",
    ],
    entry_points={
        'console_scripts': [
            'thallu = thallu:main',
        ],
    },
)
