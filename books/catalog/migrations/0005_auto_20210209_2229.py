# Generated by Django 3.1.5 on 2021-02-09 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20210209_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publishing_house',
            field=models.CharField(choices=[('Litera', 'Litera'), ('Nemira', 'Nemira'), ('Curtea Veche', 'Curtea veche')], max_length=100),
        ),
    ]
