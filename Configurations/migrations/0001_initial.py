# Generated by Django 4.0.6 on 2022-07-17 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='configuration',
            fields=[
                ('configurationId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Configuration Name')),
                ('accessKey', models.CharField(max_length=255, verbose_name='Access Key')),
                ('FieldType', models.CharField(choices=[('boolean', 'Boolean'), ('text', 'Text'), ('select', 'Select'), ('mailTemplate', 'Mail Template')], default='text', max_length=50, verbose_name='Field Type')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='configurationGroup',
            fields=[
                ('configurationGroupId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Group name')),
                ('sortOrder', models.IntegerField(verbose_name='Sort Order')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='configurationValue',
            fields=[
                ('configurationValueId', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=255, verbose_name='Key')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('sortOrder', models.IntegerField(verbose_name='Sort Order')),
                ('isDefault', models.BooleanField(default=False, verbose_name='Is Default')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('configurationName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Configurations.configuration')),
            ],
        ),
        migrations.AddField(
            model_name='configuration',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Configurations.configurationgroup'),
        ),
    ]
