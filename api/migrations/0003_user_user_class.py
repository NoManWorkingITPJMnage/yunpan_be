# Generated by Django 3.0.8 on 2020-08-01 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_real_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_class',
            field=models.CharField(default='', max_length=128),
        ),
    ]