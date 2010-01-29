Release procedure
-----------------

1. Make sure all tests pass.
2. Make sure the code is PEP 8 compatible.
3. Remove -dev suffix of __version__ at __init__.py
4. Build and upload packages: python setup.py bdist_wininst sdist upload
5. Update docs: python setup.py build_sphinx update_sphinx
6. Bump release number (by 0.0.1 normally) and add -dev suffix to it
