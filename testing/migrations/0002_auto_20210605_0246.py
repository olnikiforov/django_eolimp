# Generated by Django 3.2.4 on 2021-06-05 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='input_file',
            field=models.FileField(upload_to='test_files/', verbose_name='Вхідні дані'),
        ),
        migrations.AlterField(
            model_name='task',
            name='output_file',
            field=models.FileField(upload_to='test_files/', verbose_name='Розвязок'),
        ),
    ]
