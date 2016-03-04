# -*- coding: utf-8 -*-

import os, sys
import site

sys.stdout = sys.stderr

site.addsitedir('/home/goat/app/venv/lib/python2.7/site-packages')
sys.path.append('/home/goat/app/src/')

from goat.app import application as uwsgi_app

application = uwsgi_app
