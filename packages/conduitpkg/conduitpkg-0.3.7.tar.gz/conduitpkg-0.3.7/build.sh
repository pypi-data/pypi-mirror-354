rm -rf dist
python3 -m hatch build
python3 -m twine upload dist/*
