# Generated by Django 4.0.2 on 2022-05-14 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inw', '0008_alter_uploadmodel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inwmodel',
            name='quantity',
            field=models.IntegerField(default='1'),
        ),
    ]
