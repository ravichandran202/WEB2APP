# Generated by Django 4.1.7 on 2023-09-06 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web2androidapp", "0012_delete_reviews"),
    ]

    operations = [
        migrations.AddField(
            model_name="userbasicinfo",
            name="convert_limit",
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name="userbasicinfo",
            name="is_paid",
            field=models.BooleanField(default=False),
        ),
    ]
