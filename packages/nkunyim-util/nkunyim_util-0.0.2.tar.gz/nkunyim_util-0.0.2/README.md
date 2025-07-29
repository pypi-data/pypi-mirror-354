# nkunyim_util
Nkunyim utilities for common operations


## Virtual Environment
- sudo apt install python3.12-venv


## Required Packages
- sudo python3.12 -m venv ~/devspace/env/package
- source ~/devspace/env/package/bin/activate
- sudo chmod -R a+rwx ~/devspace/env/package
- pip install --upgrade pip
- pip install --upgrade build twine


## NkunyimUtil Dependencies
- sudo python3.12 -m venv ~/devspace/env/nkunyim
- source ~/devspace/env/nkunyim/bin/activate
- sudo chmod -R a+rwx ~/devspace/env/nkunyim
- pip install --upgrade pip
- pip install --upgrade Django requests cryptography djangorestframework
- pip freeze > requirements.txt


## Build Package
- python3 -m build



## Upload Package
- python3 -m twine upload dist/*