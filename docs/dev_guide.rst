Release procedure
-----------------

1. Make sure all tests pass.
2. Make sure the code is PEP 8 compatible.
3. Make sure long_description is valid ("python setup.py checkdocs")*
4. Remove -dev suffix of __version__ at __init__.py
5. Build and upload packages: "python setup.py bdist_wininst sdist upload"
6. Update docs: "python setup.py build_sphinx update_sphinx"
7. Bump release number (by 0.0.1 normally) and add -dev suffix to it

* = This requires http://pypi.python.org/pypi/collective.checkdocs/ . As
this project uses setuptools instead of distutils, it will give a harmless
warning about unknown distribution option.
