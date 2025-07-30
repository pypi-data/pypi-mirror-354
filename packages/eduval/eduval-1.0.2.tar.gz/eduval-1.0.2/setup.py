from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='eduval',
    version='1.0.2',
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords="academy, assessment, python, education, student performance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib"
    ],
    extras_require={
        "dev": [
            "pytest"
        ]
    },
    url='https://github.com/shammeer-s/CSK-Academy',
    author='Mohammed Shammeer',
    author_email='mohammedshammeer.s@gmail.com',
    description='Python library for evaluating student performance '
                'and conducting assessments',
)