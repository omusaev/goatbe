# -*- coding: utf-8 -*-

import os, sys
import site

sys.stdout = sys.stderr

site.addsitedir('../venv/lib/python2.7/site-packages')
sys.path.append('../app/')

from app import application as uwsgi_app

application = uwsgi_app
