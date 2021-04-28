from navykut import __version__ as version
from navykut import __author__ as author

from setuptools import setup,find_packages


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="Navykut",
    version=version,
    url="https://github.com/navykut/navykut",
    license="MIT",
    author=author,
    author_email="aniketsarkar@yahoo.com",
    description="Fullstack web framework using flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["flask", "django", "Navykut"],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=[ 
        
    ],
    extras_require={},
    python_requires=">=3.6,<4",
    entry_points={
        "console_scripts":[
            "navykut=navykut.__main__:_main"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: flask",
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