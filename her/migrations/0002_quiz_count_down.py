# Generated by Django 4.0.5 on 2022-07-26 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('her', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='count_down',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]