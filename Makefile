# -----------------------------------------------------------------------------------------------------------
# Filename: Makefile
#
# Purpose:  Makefile for
# - the installation of the python virtual environment and all the required packages
# - the installation of the required npm packages
# -----------------------------------------------------------------------------------------------------------


.PHONY: clean install run

clean:
# remove the virtual environment, npm modules and the database
	rm -rf server/venv
	rm -rf client/node_modules
	rm -f *.db


install: clean
# install the virtual environment and all the required packages
	python3.9 -m venv server/venv
	source server/venv/bin/activate && pip install -r server/requirements.txt

# initialize the database
	export PYTHONPATH=$(shell pwd); \
	source server/venv/bin/activate; \
	python db_utils/init_db.py

# install the required npm packages
	cd client && npm install



	