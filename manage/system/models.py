from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
import mptt
import uuid

class Documents(models.Model):
    class Meta:
        db_table = "documents"
        verbose_name = "Информация о документе"
        verbose_name_plural = "Информация о документе"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, verbose_name='Уникальный идентификатор документа')
    doc_name = models.TextField(verbose_name='Название документа')
    description = models.TextField(verbose_name='Описание документа')
    document_language = models.IntegerField(verbose_name='Язык докуменат')# validators=[document_language_validator])

    def __str__(self):
        return f"{self.id} {self.doc_name} {self.document_language}"


class Files(models.Model):
    """Модель таблицы для хранения информации о файлах."""
    class Meta:
        db_table = "files"
        verbose_name = "Информация о файлах"
        verbose_name_plural = "Информация о файлах"

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, unique=True, verbose_name="Уникальный идентификатор файла")
    id_document = models.ForeignKey(Documents, on_delete=models.RESTRICT, verbose_name='ID документа')
    file_name = models.CharField(max_length=50, unique=True, verbose_name="Имя файла")
    file = models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%D/', verbose_name='Файлы')
    file_version = models.CharField(max_length=20, verbose_name='Версия файла')
    add_data = models.DateTimeField(default=timezone.now, verbose_name='Дата добавления')
    #slug = models.SlugField(max_length=255, unique=True, db_index=True, default=True, verbose_name='URL')

    def get_html_file(self, object):
        if object.file:
            return mark_safe(f"<a href='{object.file.url}', width=400")
    def __str__(self):
        return f"{self.id} {self.file_name} {self.id_document}"



class Entities(MPTTModel):
    """Древовидная модель таблицы категорий (сущностей)"""
    class Meta:
        db_table = "entities"
        verbose_name = "Сущности"
        verbose_name_plural = "Сущности"

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, unique=True, verbose_name='Уникальный идентификатор сущности')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родитель сущности')
    ent_name = models.TextField(verbose_name='Имя сущности')
    description = models.TextField(verbose_name='Описание сущности')
    cat_file = models.ForeignKey(Files, on_delete=models.RESTRICT, null=True, verbose_name='Файл категории' )

    # slug = models.SlugField()

    def get_absolute_url(self):
        return reverse('entitie-by-category', args=[str(self.id)])

    # def get_absolute_url(self):
    #     return reverse('entitie-by-category', kwargs={"cat_id": str(self.id)})


    # class MPTTMeta:
    #     #level_attr = 'mptt_level'
    #     order_insertion_by = ['ent_name']

    #mptt.register(Entities, order_insertion_by=['ent_name'])
    def __str__(self):
        return f"{self.id} {self.parent} {self.ent_name} {self.cat_file}"



def document_language_validator(document_language):
    """Проверка на валидность для выбранного языка докумнета"""
    if document_language not in ['0', '1']:
        raise ValidationError(
            gettext_lazy('%(document_language)s is not a valid language'),
            params={'document_language': document_language},
        )


# модель документов


# модель отношений
class Relations(models.Model):
    class Meta:
        db_table = "relations"
        verbose_name = "Отношения"
        verbose_name_plural = "Отношения"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, verbose_name='Уникальный идентивикатор отношения')
    id_entities = models.ForeignKey(Entities, on_delete=models.RESTRICT, verbose_name='Идентификатор сущности')
    id_document = models.ForeignKey(Documents, on_delete=models.RESTRICT, verbose_name='Идентификатор документа')

    def __str__(self):
        return f"{self.id} {self.id_entities} {self.id_document}"



class Tags(models.Model):
    """Модель таблицы для хранения и работы с тэгами"""
    class Meta:
        db_table = "tags"
        verbose_name = "Тэги"
        verbose_name_plural = "Тэги"

    id = models.UUIDField(primary_key=True, verbose_name='Уникальный идентификатор тэга')
    tag = models.CharField(max_length=20, unique=True, verbose_name='Тэг')

    def __str__(self):
        return f"{self.id} {self.tag}"



class Tag_Relation(models.Model):
    """Модель таблицы для хранения принадлежности тегов"""
    class Meta:
        db_table = "tags_relations"
        verbose_name = "Отношение тэгов"
        verbose_name_plural = "Отношение тэгов"

    id = models.UUIDField(primary_key=True, verbose_name="Уникальный идентификатор отношения тега")
    id_tag = models.ForeignKey(Tags, on_delete=models.RESTRICT, verbose_name='ID тэга')
    id_document = models.ForeignKey(Documents, on_delete=models.RESTRICT, verbose_name='ID документа')
    id_entity = models.ForeignKey(Entities, on_delete=models.RESTRICT, verbose_name='ID сущности')

    def __str__(self):
        return f"{self.id} {self.id_tag} {self.id_document} {self.id_entity}"




class RelationsFiles(models.Model):
    class Meta:
        db_table = 'relations_files'
        verbose_name = 'Отношения сущностей с файлами'
        verbose_name_plural = 'Отношения сущностей с файлами'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True,
                          verbose_name='Уникальный идентивикатор отношения')
    id_entities = models.ForeignKey(Entities, on_delete=models.RESTRICT, verbose_name='Идентификатор сущности')
    id_file = models.ForeignKey(Files, on_delete=models.RESTRICT, verbose_name='Идентификатор документа')

    def __str__(self):
        return f"{self.id} {self.id_entities} {self.id_file}"


# модель пользователей
class Users(models.Model):
    class Meta:
        db_table = "user"
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, verbose_name="Уникальный идентификатор пользователя")
    user_name = models.CharField(max_length=30, unique=True, verbose_name='Имя пользователя')
    user_password = models.CharField(max_length=16, verbose_name='Пароль')
    password_hash = models.CharField(max_length=100, verbose_name='Хэш пароля')

    def __str__(self):
        return f"{self.id} {self.user_name}"


# модель комментариев
class Comments(models.Model):
    """Модель таблицы для хранения комментариев"""
    class Meta:
        db_table = "comments"
        verbose_name = "Комментарии"
        verbose_name_plural = "Комментарии"

    id = models.UUIDField(primary_key=True, verbose_name="Уникальный идентификатор комментария")
    id_document = models.ForeignKey(Documents, on_delete=models.RESTRICT,
                                    verbose_name='ID документа к которому добавлен комментарий')
    id_user = models.ForeignKey(Users, on_delete=models.RESTRICT,
                                verbose_name='ID пользователя, добавившего комментарий')
    comment = models.TextField(blank=True, verbose_name='Комментарий к документу')
    comment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления комментария')

    def __str__(self):
        return f"{self.id} {self.id_document} {self.id_user} {self.comment}"


# валидация для прав доступа
def group_rights_validator(group_rights):
    if group_rights not in ['0', '1', '2', '3', '4']:
        raise ValidationError(
            gettext_lazy('%(group_rights)s is not a valid rights'),
            params={'group_rights': group_rights},
        )


# модель прав доступа
class Rights(models.Model):
    class Meta:
        db_table = 'rights'
        verbose_name = ("Права доступа")
        verbose_name_plural = 'Права доступа'

    id = models.IntegerField(primary_key=True, verbose_name='Идентификатор прав')
    right_number = models.IntegerField(verbose_name='Номер прав', validators=[group_rights_validator])
    rights_description = models.TextField(verbose_name='Описание права доступа')

    def __str__(self):
        return f"{self.id} {self.rights_description}"


# модель групп пользователей
class User_groups(models.Model):
    class Meta:
        db_table = "user_groups"
        verbose_name = "Группы пользователей"
        verbose_name_plural = "Группы пользователей"

    id = models.UUIDField(primary_key=True, verbose_name="Уникальный идентификатор группы пользователя")
    group_name = models.TextField(verbose_name="Наименование группы пользователя")
    group_rights = models.ForeignKey(Rights, on_delete=models.RESTRICT, verbose_name="Права для группы пользователя",
                                     validators=[group_rights_validator])

    def __str__(self):
        return f"{self.id} {self.group_rights}"


# модель доступа для разных групп пользователей
class Group_access(models.Model):
    class Meta:
        db_table = "group_access"
        verbose_name = "Доступ для конкретной группы пользователей"
        verbose_name_plural = "Доступ для конкретной группы пользователей"

    id = models.UUIDField(primary_key=True, verbose_name="Права группы пользователя")
    id_user_group = models.ForeignKey(User_groups, on_delete=models.RESTRICT, verbose_name='ID группы пользователя')
    id_user = models.ForeignKey(Users, on_delete=models.RESTRICT, verbose_name='ID пользователя')

    def __str__(self):
        return f"{self.id} {self.id_user_group}"




