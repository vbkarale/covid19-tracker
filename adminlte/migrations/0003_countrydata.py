# Generated by Django 2.2.3 on 2020-04-12 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminlte', '0002_indiadata'),
    ]

    operations = [
        migrations.CreateModel(
            name='Countrydata',
            fields=[
                ('id', models.AutoField(auto_created=True,primary_key=True, serialize=False, verbose_name='ID')),
                ('country_id', models.IntegerField(default=0)),
                ('confirmed', models.BigIntegerField(blank=True, null=True)),
                ('deaths', models.BigIntegerField(blank=True, null=True)),
                ('recovered', models.BigIntegerField(blank=True, null=True)),
                ('date', models.DateField()),
            ],
        ),
    ]
