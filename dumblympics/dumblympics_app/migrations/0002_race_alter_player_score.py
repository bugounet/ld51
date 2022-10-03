# Generated by Django 4.1.1 on 2022-10-01 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dumblympics_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open', models.BooleanField()),
            ],
        ),
        migrations.AlterField(
            model_name='player',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]