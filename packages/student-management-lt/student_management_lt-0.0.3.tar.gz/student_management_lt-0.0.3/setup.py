from setuptools import setup, find_packages

setup(
    name="student-management-lt",
    version="0.0.3",
    description="A desktop PyQt6 GUI app for managing university student data with an SQL database backend.", # Optional
    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    #
    # Often, this is the same as your README, so you can just read it in from
    # that file directly (as we have already done above)
    #
    # This field corresponds to the "Description" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=open("README.md", encoding="utf-8").read(),  # Optional
    # Denotes that our long_description is in Markdown; valid values are
    # text/plain, text/x-rst, and text/markdown
    #
    # Optional if long_description is written in reStructuredText (rst) but
    # required for plain-text or Markdown; if unspecified, "applications should
    # attempt to render [the long_description] as text/x-rst; charset=UTF-8 and
    # fall back to text/plain if it is not valid rst" (see link below)
    #
    # This field corresponds to the "Description-Content-Type" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    # This should be a valid link to your project's main homepage.
    #
    # This field corresponds to the "Home-Page" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    url="https://github.com/ltuala/student-management",  # Optional
    # This should be your name or the name of the organization which owns the
    # project.
    author="Lyndon Tuala",  # Optional
    # This should be a valid email address corresponding to the author listed
    # above.
    author_email="lyndontuala@gmail.com",  # Optional
    packages=find_packages(),
    install_requires=[
        "PyQt6",
        "python-dotenv"
    ],
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    "Development Status :: 3 - Alpha",
    # Indicate who your project is intended for
    "Intended Audience :: Developers",
    # Pick your license as you wish
    "License :: OSI Approved :: MIT License",
    # Specify the Python versions you support here. In particular, ensure
    # that you indicate you support Python 3. These classifiers are *not*
    # checked by 'pip install'. See instead 'python_requires' below.
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    ],
    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={  # Optional
    "Bug Reports": "https://github.com/ltuala/student-management/issues",
    "Source": "https://github.com/ltuala/student-management/",
    },
)