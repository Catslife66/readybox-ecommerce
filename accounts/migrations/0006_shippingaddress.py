# Generated by Django 4.2 on 2023-05-04 21:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_delete_shippingaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('postcode', models.CharField(max_length=10)),
                ('address1', models.CharField(max_length=80)),
                ('address2', models.CharField(blank=True, max_length=80, null=True)),
                ('town', models.CharField(max_length=80)),
                ('contact_number', models.CharField(max_length=20)),
                ('remarks', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
