# Generated by Django 2.2.3 on 2020-04-19 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminlte', '0004_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dailydata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_id', models.IntegerField(default=0)),
                ('cases', models.BigIntegerField(null=True)),
                ('date', models.DateField()),
            ],
        ),
    ]
