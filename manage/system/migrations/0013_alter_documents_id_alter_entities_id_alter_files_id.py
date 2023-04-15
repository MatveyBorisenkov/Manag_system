# Generated by Django 4.1.5 on 2023-04-08 15:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0012_alter_entities_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='Уникальный идентификатор документа'),
        ),
        migrations.AlterField(
            model_name='entities',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='Уникальный идентификатор сущности'),
        ),
        migrations.AlterField(
            model_name='files',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='Уникальный идентификатор файла'),
        ),
    ]
