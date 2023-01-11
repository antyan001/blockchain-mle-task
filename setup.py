from pathlib import Path
from typing import Dict

from setuptools import find_packages, setup

_HERE = Path(__file__).parent
_PATH_VERSION = _HERE / "blockchain_task" / "__version__.py"

about: Dict[str, str] = dict()
exec(_PATH_VERSION.read_text(), about)

long_description = Path(_HERE, "README.md").read_text()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT Licence",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    keywords="",
    author=about["__author__"],
    author_email="",
    license="",
    python_requires=">=3.8",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={},
)
