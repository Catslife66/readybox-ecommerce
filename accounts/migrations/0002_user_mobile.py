# Generated by Django 4.2 on 2023-04-20 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mobile',
            field=models.CharField(default=1234, max_length=11),
            preserve_default=False,
        ),
    ]
