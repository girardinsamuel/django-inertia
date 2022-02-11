from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="django-inertia",
    version="1.0.1",
    packages=find_packages(),
    description="Server-side Django adapter for Inertia.js",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # The project's main homepage.
    url="https://github.com/girardinsamuel/django-inertia",
    # Author details
    author="Samuel Girardin",
    author_email="samuelgirardin@pm.me",
    # Choose your license
    license="MIT license",
    # If your package should include things you specify in your MANIFEST.in file
    # Use this option if your package needs to include files that are not python files
    # like html templates or css files
    include_package_data=True,
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
    ],
    # What does your project relate to?
    keywords="Django, Python, Inertia.js",
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "django>=3,<4",
        "dotty-dict==1.3.0",
    ],
    python_requires=">=3.7.0",
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # $ pip install your-package[dev,test]
    extras_require={
        "dev": [
            "black",
            "flake8",
            "flake8-isort",
            "twine",
            "wheel",
            "pytest",
            "pytest-django",
            "pytest-cov",
            "coverage",
            "bump2version",
        ],
    },
)
