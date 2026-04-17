# manually created; pls do not delete

from django.db import migrations

def call_service(apps, schema_editor):
    from idea_forum.services import CreateForumContainers

    CreateForumContainers.execute({})

class Migration(migrations.Migration):

    dependencies = [
        ('idea_forum', '0001_initial'),
        # make sure django has applied the last migration in machina's forum app before running this one
        ('forum', '0012_alter_forum_id'),
    ]

    operations = [
        migrations.RunPython(call_service, reverse_code=migrations.RunPython.noop), # note: reversing the migration isn't implemented (data seeding)
    ]
