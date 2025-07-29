# Install from PyPi
`pip install zikomo`

# Install CLI from source
`pip install .`

# Uninstall
`pip uninstall zikomo`

# COMMANDS
`zikomo deploy --staging --project=backoffice`
`zikomo deploy --staging --project=websites`
`mini update log database on staging`
`zikomo --help`
`pip show zikomo`

# Distribute package
#### Run the commands from the directory where `setup.py` is available
1. `pip install twine build`
2. `python -m build`
3. `twine upload dist/*`

### PyPi URL
`https://pypi.org/project/zikomo/1.0.0/`





# Test directly
python __main__.py deploy --staging --project=backoffice
