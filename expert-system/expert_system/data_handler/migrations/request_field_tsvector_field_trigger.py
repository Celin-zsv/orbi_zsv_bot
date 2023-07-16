#
# Danger Zone!
#
# Do not remove this migration, Django won't recreate it!
#
# This migration is necessary for the the `find_closest_request` function and creates
# a PostgreSQL trigger to update tsvectors upon creating and updating user queries
# in data_handler_request table.
# This migration is not created automatically by Django and therefore it's manually
# created and depends on the `0001_initial` migration.

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("data_handler", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                 CREATE TRIGGER tsv_column_trigger
                 BEFORE INSERT OR UPDATE OF request, tsv
                 ON data_handler_request
                 FOR EACH ROW EXECUTE PROCEDURE
                 tsvector_update_trigger(
                   tsv, 'pg_catalog.russian', request
                 );

                 UPDATE data_handler_request SET tsv = NULL;
               ''',

            reverse_sql='''
                 DROP TRIGGER IF EXISTS tsv_column_trigger
                 ON data_handler_request;
               '''
        ),
    ]
