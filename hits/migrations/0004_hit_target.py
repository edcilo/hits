# Generated by Django 3.1.6 on 2021-02-05 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hits', '0003_auto_20210204_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='hit',
            name='target',
            field=models.CharField(default='unknow', max_length=255),
            preserve_default=False,
        ),
    ]
