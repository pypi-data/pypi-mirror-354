remove the existing package: rm -rf build/ dist/ *.egg-info
build again: python -m build 

upload to pypi: twine upload dist/* 