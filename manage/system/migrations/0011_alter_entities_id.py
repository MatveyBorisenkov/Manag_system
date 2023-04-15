# Generated by Django 4.1.5 on 2023-04-07 19:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0010_alter_entities_level_alter_entities_tree_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entities',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Уникальный идентификатор сущности'),
        ),
    ]
