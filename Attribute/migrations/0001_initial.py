# Generated by Django 4.0.6 on 2022-07-15 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Language', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='attribute',
            fields=[
                ('attributeId', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('inputType', models.CharField(choices=[('boolean', 'Boolean'), ('checkbox', 'Checkbox'), ('multiselect', 'Multi-select'), ('select', 'Select'), ('radio', 'Radio'), ('textbox', 'Textbox'), ('textarea', 'Textarea')], default='text', max_length=50, verbose_name='Type')),
                ('isRequired', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='yes', max_length=10, verbose_name='Required')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='option',
            fields=[
                ('optionId', models.AutoField(primary_key=True, serialize=False)),
                ('customOption', models.CharField(max_length=100, unique=True, verbose_name='Custom Option')),
                ('sortOrder', models.IntegerField(default=1, verbose_name='Sort Order')),
                ('isDefault', models.BooleanField(default=False, verbose_name='Is Default')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Attribute.attribute')),
            ],
        ),
        migrations.CreateModel(
            name='optionTranslation',
            fields=[
                ('optionTranslationId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Language.language')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Attribute.option')),
            ],
        ),
        migrations.CreateModel(
            name='attributeTranslation',
            fields=[
                ('attributeTranslationId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Attribute.attribute')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Language.language')),
            ],
        ),
    ]