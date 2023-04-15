# Generated by Django 4.1.7 on 2023-04-04 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_alter_entities_level_alter_entities_tree_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entities',
            name='level',
            field=models.PositiveIntegerField(db_index=True, verbose_name='Уровень'),
        ),
        migrations.AlterField(
            model_name='entities',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, verbose_name='Уровень вложенности'),
        ),
    ]
