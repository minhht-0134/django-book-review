# Generated by Django 3.0.4 on 2020-04-21 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='link_action',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
