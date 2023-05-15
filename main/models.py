from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import *
from django.db.models.signals import post_save


class AdvUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Пройшов активацію?')
    send_messages = models.BooleanField(default=True, verbose_name='Надіслати сповіщення про нові коментарі?')

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass



class Rubric(models .Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Назва')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, null=True, blank=True,
                                     verbose_name='Надрубрика')


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)

class SuperRubric(Rubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        return f'{self.super_rubric.name} - {self.name}'

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'


class Bb(models.Model):
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=40, verbose_name='Товар')
    content = models.TextField(verbose_name='Опис')
    price = models.FloatField(default=0, verbose_name='Ціна')
    currency_choice = (
        ('UAH', 'UAH'),
        ('USD', 'USD'),
        ('EUR', 'EUR')
    )
    currency = models.CharField(max_length=10, choices=currency_choice, blank=True, default=None, verbose_name='Валюта')

    contacts = models.TextField(verbose_name=' Контакти')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Зображення')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Автор оголошення')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Виводити у списку?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубліковано')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Оголошення'
        verbose_name_plural = 'Оголошення'
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models. CASCADE, verbose_name='Оголошення')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Зображення')

    class Meta:
        verbose_name_plural = 'Додаткові ілюстрації'
        verbose_name = 'Додаткова ілюстрація'


class Comment(models.Model):
    bb = models.ForeignKey(Bb,  on_delete=models.CASCADE, verbose_name='Оголошення')
    author = models.CharField(max_length=30, verbose_name='Автор')
    content = models.TextField(verbose_name='Зміст')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Виводити на екран?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубліковано')

    def __str__(self):
        return f'{self.bb.title} - {self.bb.author}'


    class Meta:
        verbose_name_plural = 'Комментарі'
        verbose_name = 'Комментар'
        ordering = ['created_at']


def post_save_dispatcher(sender, **kwargs):
    author = kwargs['instance'].bb.author
    if kwargs['created'] and author.send_messages:
        send_new_comment_notification(kwargs['instance'])

post_save.connect(post_save_dispatcher, sender=Comment)
