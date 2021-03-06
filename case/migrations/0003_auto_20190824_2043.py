# Generated by Django 2.1.7 on 2019-08-24 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0002_auto_20190824_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='case_number',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='case_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_number',
            field=models.IntegerField(),
        ),
    ]
