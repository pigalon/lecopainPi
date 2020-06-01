deactivate
rm -rf env/
virtualenv env/
source env/bin/activate
env/bin/python -m pip install --upgrade pip
env/bin/pip install -r requirements/dev.txt