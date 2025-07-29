"""Setup script for keyframe-scout"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read version
version_file = this_directory / "src" / "keyframe_scout" / "__init__.py"
version = None
for line in version_file.read_text().splitlines():
    if line.startswith("__version__"):
        version = line.split('"')[1]
        break

setup(
    name="keyframe-scout",
    version=version,
    author="Jiajun Chen",
    author_email="cjj198909@gmail.com",
    description="Intelligent video keyframe extraction tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cjj198909/keyframe-scout",
    project_urls={
        "Bug Tracker": "https://github.com/cjj198909/keyframe-scout/issues",
        "Documentation": "https://github.com/cjj198909/keyframe-scout#readme",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "Pillow>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.910",
            "pre-commit>=2.15",
        ],
    },
    entry_points={
        "console_scripts": [
            "keyframe-scout=keyframe_scout.__main__:main",
        ],
    },
)