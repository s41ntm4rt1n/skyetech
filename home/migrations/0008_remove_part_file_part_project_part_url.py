# Generated by Django 4.2.3 on 2023-11-30 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_project_client_project_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part',
            name='file',
        ),
        migrations.AddField(
            model_name='part',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.project'),
        ),
        migrations.AddField(
            model_name='part',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]