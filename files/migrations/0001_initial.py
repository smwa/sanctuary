# Generated by Django 2.2.2 on 2019-06-28 17:14

from django.db import migrations, models
import django.db.models.deletion
import files.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md5', models.CharField(max_length=40)),
                ('size', models.IntegerField()),
                ('content', models.FileField(upload_to=files.models.uploadTo)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=64)),
                ('hash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.Hash')),
            ],
        ),
    ]
