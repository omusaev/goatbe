# -*- coding: utf-8 -*-

import os
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_dir)

import settings as app_settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# fileConfig(config.config_file_name, disable_existing_loggers=False)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

from db.base import get_base_for_migrations

target_metadata = get_base_for_migrations().metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """

    url = app_settings.DB_CONNECTION_URL

    context.configure(url=url)

    with context.begin_transaction():
        context.run_migrations()


def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name in app_settings.ALEMBIC_EXCLUDE_TABLES:
        return False
    else:
        return True


def run_migrations_online():
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    cnf = config.get_section(config.config_ini_section)
    cnf["sqlalchemy.url"] = app_settings.DB_CONNECTION_URL

    engine = engine_from_config(
        cnf,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=include_object,
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
