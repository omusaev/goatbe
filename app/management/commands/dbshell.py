# -*- coding: utf-8 -*-

import os
import sys

from management.commands import BaseCommand
from settings import DATABASE


class Command(BaseCommand):
    help = 'Run database shell.'

    options = {}

    @classmethod
    def run(cls):
        executable = 'psql'

        args = [executable]
        args += ["-U", DATABASE.get('USERNAME')]
        args.extend(["-h", DATABASE.get('HOST')])
        args.extend(["-p", str(DATABASE.get('PORT'))])

        args += [DATABASE.get('DATABASE')]

        os.environ['PGPASSWORD'] = DATABASE.get('PASSWORD')

        if os.name == 'nt':
            sys.exit(os.system(" ".join(args)))
        else:
            os.execvp(executable, args)
