# Generated by Django 4.1.1 on 2023-07-24 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0002_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='nome',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]