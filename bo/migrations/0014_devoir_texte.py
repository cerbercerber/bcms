# Generated by Django 2.0.5 on 2018-12-12 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bo', '0013_remove_cours_duplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='devoir',
            name='texte',
            field=models.CharField(default=None, max_length=1000),
            preserve_default=False,
        ),
    ]
