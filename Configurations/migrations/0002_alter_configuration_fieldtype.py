# Generated by Django 4.0.6 on 2022-07-17 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configurations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='FieldType',
            field=models.CharField(choices=[('text', 'Text'), ('boolean', 'Boolean'), ('select', 'Select'), ('mailTemplate', 'Mail Template')], default='text', max_length=50, verbose_name='Field Type'),
        ),
    ]
