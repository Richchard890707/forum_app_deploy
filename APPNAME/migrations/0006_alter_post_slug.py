# Generated by Django 3.2.7 on 2022-07-05 13:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('APPNAME', '0005_auto_20220608_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, default=uuid.uuid4, max_length=400, unique=True),
        ),
    ]