#!/bin/bash

pep8 --ignore=E501,E731 --exclude  venv,logs,qa_auto,migrations,settings,locale,tests,docs,wsgi.py,settings_local.py --show-source --statistics --count .
