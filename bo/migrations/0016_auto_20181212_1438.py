# Generated by Django 2.0.5 on 2018-12-12 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bo', '0015_controle_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='absence',
            name='texte',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='controle',
            name='texte',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='devoir',
            name='texte',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]