# Generated by Django 3.2.13 on 2022-05-24 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipelib', '0006_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='placeholder_url',
            field=models.CharField(default='https://www.palomacornejo.com/wp-content/uploads/2021/08/no-image.jpg', max_length=200),
        ),
    ]