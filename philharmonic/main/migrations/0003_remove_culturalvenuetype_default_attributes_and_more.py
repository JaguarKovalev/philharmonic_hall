# Generated by Django 5.1.1 on 2024-09-24 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_culturalvenuetype_alter_culturalvenue_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="culturalvenuetype",
            name="default_attributes",
        ),
        migrations.AddField(
            model_name="culturalvenuetype",
            name="attributes_list",
            field=models.JSONField(default=list),
        ),
    ]
