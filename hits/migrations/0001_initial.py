# Generated by Django 3.1.6 on 2021-02-04 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('c', 'Closed'), ('f', 'Failed'), ('o', 'Open')], default='o', max_length=1)),
            ],
        ),
    ]