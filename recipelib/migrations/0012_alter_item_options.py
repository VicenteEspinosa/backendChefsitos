# Generated by Django 3.2.13 on 2022-05-25 01:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipelib', '0011_recipe_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['order_number']},
        ),
    ]