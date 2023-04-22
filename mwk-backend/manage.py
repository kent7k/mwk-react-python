import os
import sys

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    # --------------- when using postgresql ---------------
    # Note: Nothing to do here
    # -----------------------------------------------------

    # ---------------- when using mysql -------------------
    # try:
    #     from django.db.backends.mysql.schema import DatabaseSchemaEditor
    #
    #     DatabaseSchemaEditor.sql_create_table += ' ROW_FORMAT=DYNAMIC'
    # except ImportError:
    #     pass
    # -----------------------------------------------------

    execute_from_command_line(sys.argv)
