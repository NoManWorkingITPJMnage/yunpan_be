# Generated by Django 3.0.8 on 2020-08-01 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_user_class'),
    ]

    operations = [
        migrations.CreateModel(
            name='Floder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floder_name', models.CharField(max_length=256, unique=True)),
                ('creator', models.CharField(max_length=128)),
            ],
        ),
    ]