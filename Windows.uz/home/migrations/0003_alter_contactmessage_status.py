# Generated by Django 3.2.6 on 2021-08-21 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210821_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmessage',
            name='status',
            field=models.CharField(choices=[('New', 'Yangi'), ('Read', "O'qilgan"), ('CLosed', 'Yopilgan')], default='New', max_length=10),
        ),
    ]