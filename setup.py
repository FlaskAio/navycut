from navycut import __version__ as version
from navycut import __author__ as author

from setuptools import setup,find_packages

import os as os

basedir = os.path.abspath(os.path.dirname(__file__))


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="Navycut",
    version=version,
    url="https://github.com/flaskAio/navycut",
    license="MIT",
    author=author,
    author_email="aniketsarkar@yahoo.com",
    description="Fullstack web framework using flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["flask", "django", "Navycut"],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=[ 
        "Flask-Admin>=1.5.8",
        "Flask-Bootstrap>=3.3.7.1",
        "Flask-Cors>=3.0.10",
        "flask-mailman>=0.3.0",
        "Flask-Login>=0.5.0",
        "Flask-Migrate>=2.7.0",
        "Flask-SQLAlchemy>=2.5.1",
        "Flask-WTF>=0.15.1",
        "nc-console>=0.0.4",
        "python-dotenv>=0.17.1",
        "SQLAlchemy-JSONField>=1.0.0",
        "WTForms<=2.3.3",
        "WTForms-SQLAlchemy>=0.2",
        "pillow>=8.3.0",
        "Flask-Express>=0.1.1" # flask-express will maintain the default flask package and it's version.
    ],
    extras_require={},
    python_requires=">=3.6,<4",
    entry_points={
        "console_scripts":[
            "navycut=navycut.__main__:_main"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)