# Generated by Django 2.0.5 on 2018-11-26 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bo', '0010_auto_20181114_1356'),
    ]

    operations = [
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('JUSTI', 'Justifié'), ('PASJU', 'Pas justifié')], default='PASJU', max_length=5)),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bo.Cours')),
                ('eleve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bo.Eleve')),
            ],
        ),
        migrations.CreateModel(
            name='Devoir',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('NOTE', 'Noté'), ('PANO', 'Pas noté')], default='PANO', max_length=4)),
                ('bareme', models.CharField(blank=True, choices=[('VIN', '20'), ('DIX', '10')], default='VIN', max_length=3, null=True)),
                ('cours', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bo.Cours')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.FloatField()),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bo.Cours')),
                ('eleve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bo.Eleve')),
            ],
        ),
    ]