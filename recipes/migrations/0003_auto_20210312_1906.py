# Generated by Django 3.1.7 on 2021-03-13 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20210305_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(help_text='Describe your recipe in a sentence or two.'),
        ),
    ]