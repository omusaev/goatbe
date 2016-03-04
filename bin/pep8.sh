#!/bin/bash

pep8 --ignore=E501,E731 --exclude  virtualenv,logs,qa_auto,migrations,settings,locale,tests,docs,wsgi.py,urls.py,settings_local.py --show-source --statistics --count .
