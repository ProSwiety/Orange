# Generated by Django 4.0.2 on 2022-04-16 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inw', '0002_rename_ean_inwmodel_ean_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='inwmodel',
            unique_together={('Nazwa', 'EAN', 'Ilosc')},
        ),
    ]
